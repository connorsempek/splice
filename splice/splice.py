# parent class of all splice objects in splice_objs.py

# imports
import json
import itertools
import plotly.graph_objs as go
from splicers import * # FIX THIS!
from colors import *

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
        self.colors = get_color_blob()
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
        '''makes subplots for each val in traces.keys()
        
        Parameters
        ----------
        cols     : (int) number of columns in the array of subplots
        ordering : (list) complete list of idx values, the order of which determines the 
                   order (left to right, top to bottom) the subplots will be displayed
        **kwargs : plotly.tools.make_subplots keyword arguments
        
        Returns
        -------
        plotly Figure with subplot data, and layout object matched to the state of 
        self.layout at runtime
        '''
        
        fig = make_subplots(
            traces=self.traces, cols=cols, ordering=ordering, **kwargs)
        
        # make sure current layout is
        for k, v in self.layout.items():
            if k not in fig['layout'].keys():
                fig['layout'][k] = v
        return fig
        
    
    def _get_slices(self):
        
        unique_vals = [self.df[col].unique() for col in self.slice_by]
        return itertools.product(*unique_vals)
        
    
    def _update_trace_attrs(self):
        '''default trace attributes that I think are most pleasing
        '''
        
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


    def update_traces(self, names=None, **attrs):
        '''update trace attributes after object instantiation
        
        Parameters
        ----------
        names: (list) list of trace names to update, defaults to updating all traces
        '''
        
        for idx, trace_list in self.traces.items(): 
            for trace in trace_list:
                    
                name = trace['name']
                if names:
                    if name in set(names):
                        trace.update({k: v for k, v in attrs.items()})
                else:
                    trace.update({k: v for k, v in attrs.items()})
                    
                if 'xaxis' in trace.keys():
                    del trace['xaxis']
                
                if 'yaxis' in trace.keys():
                    del trace['yaxis']
        
        self._set_layout()
        self._set_figure()
                    