import bokeh
from bokeh.plotting import figure #, show
from bokeh.models import ColumnDataSource, HoverTool, Span
from bokeh.embed import components
import scipy.stats as stats
from scipy.integrate import quad
import numpy as np

# A collection of stats calculators developped in the context of STAB22 at UTSC.
def normalProbabilityDensity(x):
    constant = 1.0 / np.sqrt(2*np.pi)
    return(constant * np.exp((-x**2) / 2.0) )

def z_score(raw, mean, std):
    '''Calculator showing the probability corresponding to a certain Z-score.'''

    # Set up our x-axis
    x_ax = np.linspace(-4, 4, 100)

    # Our normal curve
    curve = stats.norm.pdf(x_ax, 0, 1)

    # Z-score
    z = (float(raw) - float(mean))/float(std)
    cum_dist = Span(location=z, dimension='height', line_color='red',
                    line_dash='dashed', line_width=2)
    cum_dist.level = 'underlay'

    z_percentile = quad(normalProbabilityDensity, np.NINF, z)

    x = round(z_percentile[1]*100)
    intercept = normalProbabilityDensity(z)#(curve[min(99,x)]) # + ((curve[min(99,x+1)] - curve[x])/2))

    # Set up the chart
    tools = []
    p = figure(tools=tools, x_range=(-4,4), y_range=(0, 0.5),
        background_fill_color="#E1E6DC", border_fill_color="#E1E6DC",
        outline_line_color="#E1E6DC", plot_width=900, plot_height=450,
        sizing_mode='scale_width', )#border_fill_alphaa=0,)

    p.xaxis.visible = False
    p.yaxis.visible = False
    p.grid.visible = False
    p.toolbar.logo = None
    p.toolbar_location = None

    # Draw our elements
    p.add_layout(cum_dist)
    p.line(x_ax, curve, line_width=4, color='#7F8496')
    p.circle(z, intercept, line_width=16, color='#7F8496')
    
    
    script, div = components(p)

    return (z, z_percentile), script, div
