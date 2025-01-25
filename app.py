import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def load_election_data():
    
    file_path = "31_Winning_Candidate_Analysis_Over_Total_Electors.csv"
    
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
        print(f"Current working directory: {os.getcwd()}")
        print("Please make sure the CSV file is in the same directory as this script.")
        return None
    
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def create_visualization(df):
    if df is None:
        return
        
    
    percentage_columns = [
        'Winner with <= 10%',
        'Winner with > 10% to <= 20%',
        'Winner with > 20% to <=30%',
        'Winner with >30% to <=40%',
        'Winner with >40% to <=50%',
        'Winner with >50% to <=60%',
        'Winner with >60% to <=70%',
        'Winner with > 70%'
    ]
    
    
    fig = go.Figure()
    
    
    colors = px.colors.qualitative.Set3
    
    for i, column in enumerate(percentage_columns):
        fig.add_trace(go.Bar(
            name=column.replace('Winner with ', ''),
            x=df['Name of State/UT'],
            y=df[column],
            text=df[column],
            textposition='outside',
            marker_color=colors[i % len(colors)],
            hovertemplate="<b>%{x}</b><br>" +
                         "Seats: %{y}<br>" +
                         "Range: " + column.replace('Winner with ', '') +
                         "<extra></extra>"
        ))

    
    fig.update_layout(
        title={
            'text': 'Distribution of Winning Margins Across States/UTs (2024)',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24)
        },
        xaxis_title='<b>State/UT</b>',
        yaxis_title='<b>Number of Seats</b>',
        barmode='group',
        xaxis_tickangle=-45,
        height=900,  
        width=1200,  
        showlegend=True,
        legend_title='<b>Winning Margin</b>',
        legend={
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': 'rgba(0,0,0,0.2)',
            'borderwidth': 1
        },
        margin=dict(b=100, t=120, l=80, r=80),
        hovermode='x unified',
        plot_bgcolor='rgba(250,250,250,0.9)',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif")
    )
    
    
    fig.update_yaxes(
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='rgba(0,0,0,0.2)'
    )
    
    
    for i, state in enumerate(df['Name of State/UT']):
        total_seats = df.loc[df['Name of State/UT'] == state, 'No. Of Seats'].values[0]
        fig.add_annotation(
            x=state,
            y=max([df.loc[df['Name of State/UT'] == state, col].values[0] for col in percentage_columns]),
            text=f'<b>Total Seats: {total_seats}</b>',
            showarrow=False,
            yshift=20,
            font=dict(size=10, color='rgba(0,0,0,0.6)')
        )

    fig.show()

def main():
    df = load_election_data()
    create_visualization(df)

if __name__ == "__main__":
    main()
