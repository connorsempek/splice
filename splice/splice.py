# parent class of all splice objects in splice_objs.py

# imports
import json
import itertools
import plotly.graph_objects as go


class Splice(object):
    
    def __init__(self, df, plot_func, x, y, slice_by, idx, hover_text, 
                 color=None, group_legend=True, **kwargs):
        
        # instantiate parameters to class attributes
        self.df = df
        self.plot_func = plot_func
        self.x = x
        self.y = y
        self.slice_by = slice_by
        self.idx = idx
        self.hover_text = hover_text
        self.kwargs = {k:v for k,v in kwargs.iteritems()}
        
        # build traces
        self.traces = spliced_traces(
            df=self.df,
            plot_func=self.plot_func,
            x=self.x, 
            y=self.y, 
            slice_by=self.slice_by,
            idx=self.idx,
            hover_text=self.hover_text,
            **self.kwargs)
        
        # get slices
        self.slices = list(self._get_slices())
        
        # flat ui colors
        if colors:
            self.colors = {slc: self.df.loc[]}
        with open('flat_ui_colors.json', 'r') as f:
            self.colors = json.load(f)
        self.color_map = make_rgba_color_map(self.slices, seed=111)
        
        # update trace colors with flat ui, group and format legend
        self._update_trace_attrs()
        
        # initialize layout and figure
        self._set_layout() 
        self._set_figure()
        
        
    def _set_layout(self):
        '''creates layout object
        '''
        
        # instantiate layout object
        self.layout = go.Layout()
        
        # remove legend gaps
        self.layout.update({'legend': {'tracegroupgap':0}})
    
    
    def _set_figure(self):
        
        # instantiate figure object
        self.figure = make_figure(self.traces)
        
        # update figure with layout if it has been instantiated
        self.figure.update({'layout': self.layout})
            
    
    def update_layout(self, **kwargs):
        
        self.layout.update(**kwargs)
    
    
    def update_figure(self, **kwargs):
        
        self.figure.update(**kwargs)
    
    
    def subplots(self, cols=None, ordering=None, **kwargs):
        
        self.subplot_figure = make_subplots(
            traces=self.traces, cols=cols, ordering=ordering, **kwargs)
        
        for k, v in self.layout.items():
            if k not in self.subplot_figure['layout'].keys():
                self.subplot_figure['layout'][k] = v
        
    
    def _get_slices(self):
        
        unique_vals = [self.df[col].unique() for col in self.slice_by]
        return itertools.product(*unique_vals)
        
    
    def _update_trace_attrs(self):
        
        legend_keys = set([])
        for idx, trace_list in self.traces.items():
            for trace in trace_list:

                name = trace['name']
                
                # update color
                color = self.color_map[tuple(name.split('|'))]
                marker = {'color': color}
                trace.update({'marker': marker})
                
                # group legend
                if name in legend_keys:
                    trace.update({'legendgroup': name, 'showlegend': False})
                else:
                    trace.update({'legendgroup': name})
                    legend_keys.add(name)
                    