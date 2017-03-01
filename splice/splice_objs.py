# subclasses of Splice for specific plot types


class Lines(Splice):
    '''spliced version of plotly.graph_objs.Scatter with mode='lines'
    '''
    def __init__(self, df, x, y, slice_by, idx, hover_text, **kwargs):
        
        Splice.__init__(self, df=df, plot_func=go.Scatter, x=x, y=y,
            slice_by=slice_by, idx=idx, hover_text=hover_text, mode='lines', 
            **kwargs)
    
        
class Points(Splice):
    '''spliced version of plotly.graph_objs.Scatter with mode='markers'
    '''
    def __init__(self, df, x, y, slice_by, idx, hover_text, **kwargs):
        
        Splice.__init__(self, df=df, plot_func=go.Scatter, x=x, y=y,
            slice_by=slice_by, idx=idx, hover_text=hover_text, mode='markers', 
            **kwargs)

        
class Bars(Splice):
    '''spliced version of plotly.graph_objs.Bar
    '''
    def __init__(self, df, x, y, slice_by, idx, hover_text, **kwargs):
        
        Splice.__init__(self, df=df, plot_func=go.Bar, x=x, y=y,
            slice_by=slice_by, idx=idx, hover_text=hover_text, **kwargs)


class StackedBars(Splice):
    '''spliced version of plotly.graph_objs.Bar with barmode='stack' set in
    the layout object
    '''
    def __init__(self, df, x, y, slice_by, idx, hover_text, **kwargs):
        
        Splice.__init__(self, df=df, plot_func=go.Bar, x=x, y=y,
            slice_by=slice_by, idx=idx, hover_text=hover_text, **kwargs)
        
        self.update_layout(barmode='stack')
        self.update_figure(layout=self.layout)

        
class GroupedBars(Splice):
    '''spliced version of plotly.graph_objs.Bar with barmode='group' set in
    the layout object
    '''
    def __init__(self, df, x, y, slice_by, idx, hover_text, **kwargs):
        
        Splice.__init__(self, df=df, plot_func=go.Bar, x=x, y=y,
            slice_by=slice_by, idx=idx, hover_text=hover_text, **kwargs)
        
        self.update_layout(barmode='group')
        self.update_figure(layout=self.layout)
