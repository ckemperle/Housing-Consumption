def plot(type='line'):
    if type == 'line':
        try:
            names=list(df.columns.values)
            names.insert(1,'Aggregation Cold Water + Hot Water')
            names.insert(3,None)
            fig = make_subplots(rows=len(df.columns), cols=2,  subplot_titles=(names))
            fig.add_trace(go.Scatter(x=df.index, y=df['ColdWater'], name='Cold Water Consumption'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['HotWater'], name='Hot Water Consumption'), row=2, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['HeatingConsumption'], name='Heating Consumption'), row=3, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['ColdWater']+df['HotWater'], name='Aggregation'), row=1, col=2)
            fig.update_layout(autosize=False,
                              width=1200,
                              height=700,
                              showlegend=False)
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="m^3", row=1, col=1)
            fig.update_yaxes(title_text="m^3", row=2, col=1)
            fig.update_yaxes(title_text="MWh", row=3, col=1)
            fig.update_xaxes(title_text="Date", row=2, col=2)
            fig.update_yaxes(title_text="m^3", row=2, col=2)
            fig.show()
        except Exception as err:
            print(err)
            print(f'Some error occurred...')

    if type == 'bar':
        try:
            dfDiff = pd.DataFrame(df.diff())
            dfDiff['Datum'] = df.index
            names=list(df.columns.values)
            names.insert(1,'Aggregation Cold Water + Hot Water')
            names.insert(3,None)
            fig = make_subplots(rows=len(df.columns), cols=2, subplot_titles=(names))
            fig.add_trace(go.Bar(x=dfDiff['Datum'], y=dfDiff['ColdWater'], name='Cold Water Consumption'), row=1, col=1)
            fig.add_trace(go.Bar(x=dfDiff['Datum'], y=dfDiff['HotWater'], name='Hot Water Consumption'), row=2, col=1)
            fig.add_trace(go.Bar(x=dfDiff['Datum'], y=dfDiff['HeatingConsumption'], name='Heating Consumption'), row=3, col=1)
            fig.add_trace(go.Bar(x=dfDiff['Datum'], y=dfDiff['ColdWater']+dfDiff['HotWater'], name='Aggregation'), row=1, col=2)
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="m^3", row=1, col=1)
            fig.update_yaxes(title_text="m^3", row=2, col=1)
            fig.update_yaxes(title_text="MWh", row=3, col=1)
            fig.update_xaxes(title_text="Date", row=1, col=2)
            fig.update_yaxes(title_text="m^3", row=1, col=2)
            fig.update_layout(autosize=False,
                              width=1200,
                              height=700,
                              showlegend=False)
            fig.show()
        except Exception as err:
            print(err)
            print(f'Some Error occured...')

def save():
    df.to_excel(f'{datetime.datetime.now().date().strftime("%d-%m-%Y")}.xlsx')


# %%

if __name__ == "__main__":
    import pickle
    import time
    import numpy as np
    import datetime
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    #open file
    with open('data/consumption.pickle', 'rb') as handle:
        df = pickle.load(handle)

    loop = True
    while loop:

        print('\n Numbers for actions: \n ------------- \n 1: New input Cold Water \n 2: New input Hot Water \n 3: New input Heating Consumption \n 4: print dataframe \n 5: save to xlsx \n 6: plot line charts \n 7: plot bar charts \n 8: exit \n ------------- \n')

        action = int(input('Number: '))

        if action == 1:
            #user input
            kaltwasser = float(input("Cold Water: "))
            date = datetime.datetime.now().date()
            try:
                df.loc[(pd.to_datetime(date), 'ColdWater')]=kaltwasser
            except:
                df = df.append(pd.DataFrame({'ColdWater':[kaltwasser]}, index=[pd.to_datetime(date)]))
            all_date = pd.date_range(start=df.index.min(), end=df.index.max())
            try:
                df = df.reindex(all_date)
            except:
                pass
            df['ColdWater'] = df['ColdWater'].interpolate(method='time')

        elif action == 2:
            #user input
            warmwasser = float(input("Hot Water: "))
            date = datetime.datetime.now().date()
            try:
                df.loc[(pd.to_datetime(date), 'HotWater')]=warmwasser
            except:
                df = df.append(pd.DataFrame({'HotWater':[warmwasser]}, index=[pd.to_datetime(date)]))
            all_date = pd.date_range(start=df.index.min(), end=df.index.max())
            try:
                df = df.reindex(all_date)
            except:
                pass
            df['HotWater'] = df['HotWater'].interpolate(method='time')

        elif action == 3:
            #user input
            heizung = float(input("Heating Consumption: "))
            date = datetime.datetime.now().date()
            try:
                df.loc[(pd.to_datetime(date), 'HeatingConsumption')]=heizung
            except:
                df = df.append(pd.DataFrame({'HeatingConsumption':[heizung]}, index=[pd.to_datetime(date)]))
            all_date = pd.date_range(start=df.index.min(), end=df.index.max())
            try:
                df = df.reindex(all_date)
            except:
                pass
            df['HeatingConsumption'] = df['HeatingConsumption'].interpolate(method='time')

        elif action == 4:
            print(df)

        elif action == 5:
            save()

        elif action == 6:
            plot(type='line')

        elif action == 7:
            plot(type='bar')

        elif action == 8:
            with open('data/consumption.pickle', 'wb') as handle:
                pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print('Saved!')
            print('BYE!')
            time.sleep(2)
            loop = False
        else:
            print(f'Sorry, no action at {action}... Try another number!')
