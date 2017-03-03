# splice
Plot multiple slices of data in plotly (more easily).

### TODOs
* Should default many parameters to None (e.g., slice_by and idx)
* Bug with empty string hover_text
* update traces method
* drop_attr method which performs an update by removing an attribute
* access trace list as attribute
* annotation methods, especially in bar charts
* break up splicer functions
* method to return traces indexed by name (might be useful)
* add points/lines e.g. add y=3 line, and allow to add by date or categorical point too
* Ribbon plots
* Error bars
* Subplots shouldn't have dedicated figure, should call an update method, or, have methods that return static figure that doesn't get updated
 