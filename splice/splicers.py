###############################################################################
# helper functions used to create spliced traces and to create plotly objects
# from the spliced traces dict structure
#------------------------------------------------------------------------------
# TODO
# * pass column name of column in df encoding color mapping
###############################################################################

# -----------------------------------------------------------------------------
# imports
import re
import itertools
import plotly
import plotly.graph_objs as go

# -----------------------------------------------------------------------------
def _spliced_traces(df, x, y,  plot_func, agg='sum', 
                  slice_by=None, filter_by=None, hover_text=None,
                  **kwargs):
    '''makes single group of traces of slices of a dataframe 
    
    Parameters
    ----------
    df: pandas dataframe
    x         : (str) column in df
    y         : (str) column in df
    plot_func : a plotting class in plotly.graph_objs which takes in 2 variables (e.g., Scatter, Bar)
    slice_by  : (list) column names in df not coinciding with x or y
    filter_by : (dict) items are pairs k, v where k is in df.columns and v is a list of values in df[k].
                All records not tied to a value in df[k] matching some value in v will be omitted.
    hover_text: (list or str) List of column names whose values are to be present in the hovertool. If a str
                is passed, then the string will be formatted according to the columns present. E.g., 
                `Column A: {colA:.2f}<br>Column B: {colB:.2%}`
    agg       : (str) how to aggregate y across slices, defaults to 'sum'. Can be any valid aggregation method
                for pandas groupby objects.
    **kwargs  : keyword args for the specified plot_func

    Returns
    -------
    list of traces, which are dicts that can be parsed by plotly go.Figure class
    '''
    
    # filter data
    if filter_by:
        filter_mask = True
        for filter_col, filter_vals in filter_by.items():
            filter_mask = filter_mask & df[filter_col].isin(filter_vals)
        df = df[filter_mask]

    # generate all possible slices
    if not slice_by:
        slice_by = []
        
    slices = itertools.product(*[df[col].unique() for col in slice_by])
    grp_cols = [x] + slice_by
    agg_cols = [y]
    
    # update stuff (what's happening here, I don't remember) 
    text_cols = []
    if hover_text:
        if isinstance(hover_text, list):
            text_cols = hover_text
        elif isinstance(hover_text, str):
            field_names = re.findall('\{(.*?)\}', hover_text)
            text_cols = map(lambda s: s.split(':')[0], field_names)
        grp_cols += [col for col in text_cols if col not in slice_by + [x, y]]        
        
    # create a trace for each slice
    traces = []
    for i, tup in enumerate(slices):

        slice_mask = [True] * df.shape[0]
        for col_name, col_val in zip(slice_by, tup):
            slice_mask = slice_mask & (df[col_name] == col_val)
        sliced_df = df[slice_mask].groupby(grp_cols)[agg_cols].agg(agg).reset_index()
        
        if not sliced_df.empty:
            trace = plot_func(
                x=sliced_df[x],
                y=sliced_df[y],
                name='|'.join(tup),
                **kwargs
                )
            
            # set hover text for slice
            if hover_text:
                
                text_tups = zip(*[sliced_df[col].values for col in text_cols])
                text_str = '<br>'.join([col + ': {}' for col in text_cols])
                text = [text_str.format(*tup) for tup in text_tups]
                if isinstance(hover_text, str):
                    text_str = hover_text
                    text = [text_str.format(**{col: tup[text_cols.index(col)] for col in text_cols}) 
                            for tup in text_tups]
                trace['text'] = text
                trace['hoverinfo'] = 'text'
            
            traces.append(trace)
            
    return sorted(traces)


def spliced_traces(df, x, y, plot_func, 
                       idx=None, slice_by=None, hover_text=None, agg='sum',
                       **kwargs):
    '''makes single group of traces of slices of a dataframe 
    
    Parameters
    ----------
    df: pandas dataframe
    x         : (str) column in df
    y         : (str) column in df
    plot_func : a plotting class in plotly.graph_objs which takes in 2 variables (e.g., Scatter, Bar)
    slice_by  : (list) column names in df not coinciding with x or y
    filter_by : (dict) items are pairs k, v where k is in df.columns and v is a list of values in df[k].
                All records not tied to a value in df[k] matching some value in v will be omitted.
    idx       : (list) column names in df not coinciding with x or y. Distinct combinations of values in columns
                passed will be shown as options in a dropdown menu
    agg       : (str) how to aggregate y across slices, defaults to 'sum'. Can be any valid aggregation method
                for pandas groupby objects.
    **kwargs  : keyword args for the specified plot_func

    Returns
    -------
    dict of traces, indexed by slice values
    '''    
    
    # create trace dictv values
    idx_vals = [idx]
    idx_filter = {}
    if idx:
        idx_vals = list(itertools.product(*[df[col].unique() for col in idx]))

    traces = {}
    filter_by = {}
    for val in idx_vals:
        
        if idx:
            for col in idx:
                filter_by[col] = [val[idx.index(col)]]
        
        filtered_traces = _spliced_traces(df=df, x=x, y=y, 
            slice_by=slice_by,
            filter_by=filter_by,
            plot_func=plot_func,
            hover_text=hover_text,
            **kwargs
            )
        
        if val:
            traces['|'.join(val)] = filtered_traces
        else:
            traces[val] = filtered_traces
    return traces


def make_buttons(traces, **kwargs):
    '''make buttons from idx parameter args
    '''

    buttons = []
    for val in traces.keys():
        args = [[key == val] * len(trace_list) for key, trace_list in traces.items()]
        button = {
            'args': ['visible', list(itertools.chain.from_iterable(args))],
            'label': val
            }
        button.update(**kwargs)
        buttons.append(button)
    return buttons


def make_subplots(traces, cols=None, ordering=None, **kwargs):
    '''make subplots from idx parameter args
    TODO
    * ability to pass relative dimension list to make_subplots()
    * how to handle straggler plots when there should be empty figures
    '''

    if cols:
        stragglers = len(traces) % cols
        rows = len(traces) / cols
        if stragglers != 0:
            rows += 1
    else:
        cols = 1
        rows = len(traces)
        
    keys = traces.keys()
    if ordering:
        keys = ordering

    fig = plotly.tools.make_subplots(rows=rows, cols=cols, subplot_titles=keys, **kwargs)
    for i, key in enumerate(keys):
        trace_list = traces[key]
        for trace in trace_list:
            fig.append_trace(trace, (i / cols) + 1, (i % cols) + 1)
    
    # delete stragglers
    if stragglers != 0:

        del_start = len(traces) + 1
        del_end = cols * rows + 1
        for i in range(del_start, del_end):
            del fig['layout']['xaxis' + str(i)]
            del fig['layout']['yaxis' + str(i)]
            
    return fig


def make_figure(traces, **kwargs):
    
    data = list(itertools.chain.from_iterable(traces.values()))
    return go.Figure(data=data, **kwargs)