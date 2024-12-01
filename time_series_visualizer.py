import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", 
                 header= 0,
                 index_col = 'date',
                 parse_dates = ['date'])

#df= df.reset_index()
# Index 
#df.index = df["date"]

# Clean data
lower_perc = df.quantile(2.5/100)["value"]
higher_perc = df.quantile(97.5/100)["value"]

df= df[ (df["value"] > lower_perc) & (df["value"] < higher_perc )]


def draw_line_plot():
    # Draw line plot

    #initiating the figure    
    #plt.figure(num=1,
    #          figsize=(8,6))
    
    fig,ax = plt.subplots(figsize = (23,9))
    ax.plot(df, color="#8B0000")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_ylabel("Page Views")
    ax.set_xlabel("Date")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    df_bar = df.groupby(df.index.to_period('M')).mean()    
    # resetting column names
    
    df_bar['Months'] = df_bar.index.to_timestamp().month_name()
    df_bar['Years'] = df_bar.index.year
    
    # setting month order because jesus this is always so complicated
    month_order = ['January', 'February', 'March','April','May','June','July', 'August', 'September','October','November', 'December']
    
    # unstacking for vis
    df_pivot = df_bar.pivot(index= 'Years', columns ='Months', values = 'value')[month_order]
    
    # renaming the column index 
    df_pivot.columns.names = ['Months']
    
    fig, ax = plt.subplots( figsize = (14,10))
    df_pivot.plot(kind="bar", ax=ax)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_box["value"] = df_box["value"].astype('float')
    df_box["month"] = df_box["month"].astype('category')    
    df_box['year'] = df_box['year'].astype('category')

    # setting month order because jesus this is always so complicated
    month_order = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul', 'Aug', 'Sep','Oct','Nov', 'Dec']
    
    # Create the plot
    fig, ax = plt.subplots(1,2, sharey=True, figsize=(21, 10))


    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    sns.boxplot(x="month", y="value", data= df_box, ax=ax[1], order = month_order)

    ax[0].set_xlabel("Year")
    ax[1].set_xlabel("Month")
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[0].set_ylabel("Page Views")    
    ax[1].set_ylabel("Page Views")    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
