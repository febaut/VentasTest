import streamlit as st
import pandas as pd
from datetime import datetime


def main():
    # Load existing sales data or create empty dataframe
    sales_data = load_sales_data()
    exp_data = load_expenditures()

    try:
        prices = pd.read_csv('prices.csv')
    except IndexError:
        st.error('Lista de precios no encontrada!')

    con1 = st.container()
    con2 = st.container()
    con3 = st.container()
    # Sidebar for user input
    with st.sidebar:
        st.title('Gestor de ventas')
        st.subheader('Ingresar Venta')
        product_name = st.selectbox('Producto', prices['Producto'], placeholder=prices['Producto'][0])
        quantity_sold = st.number_input('Cantidad', min_value=1)
        try:
            price_per_unit = st.number_input('Precio', min_value= (prices.query(f"Producto == '{product_name}'")['Precio'].iloc[0])*quantity_sold)
        except IndexError:
            price_per_unit = st.number_input('Precio', min_value= 0)
            st.error('Producto no encontrado!')
        total_venta = (price_per_unit*quantity_sold)

        if st.button('Ingresar venta'):
            add_sale(sales_data, product_name, quantity_sold, price_per_unit, total_venta)
        
        # Gastos
        st.subheader('Ingresar gasto')
        expenditure = st.number_input('Total', min_value=0)
        reason = st.text_input('Motivo', 'No especificado')

        if st.button('Ingresar gasto'):
            add_expense(exp_data, expenditure, reason)
    
        with con1:         
        #Ventas
            st.subheader('Ultimas 10 ventas')
            st.table(sales_data.head(10))
        
        with con2:         
        #Ventas
            st.subheader('Balance de Caja')
            date1 = st.date_input("Fecha")
            ventas_dia = sales_data.query(f"Fecha == '{date1}'")['Total Venta'].sum()
            gastos_dia = exp_data.query(f"Fecha == '{date1}'")['Cantidad'].sum()
            st.write(f"Total de ventas $: {ventas_dia}")
            st.write(f"Total de gastos $: {gastos_dia}")
            st.write(f"Total despues de gastos $: {ventas_dia - gastos_dia}")
        with con3:       
            st.subheader('Historial de gastos (Ultimos 10)')
            st.table(exp_data.head(10))
  

def load_sales_data():
    try:
        sales_data = pd.read_csv('sales_data.csv')
    except FileNotFoundError:
        sales_data = pd.DataFrame(columns=['Fecha', 'Hora', 'Producto', 'Cantidad', 'Precio por unidad', 'Total Venta'])
    return sales_data

def load_expenditures():
    try:
        exp_data = pd.read_csv('expenditures.csv')
    except FileNotFoundError:
        exp_data = pd.DataFrame(columns=['Fecha', 'Hora', 'Cantidad', 'Motivo'])
    return exp_data

def add_sale(dataframe, product_name, quantity_sold, price_per_unit, total_venta):
    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d")
    hour_str = current_datetime.strftime("%H:%M:%S")
    new_row = {'Fecha':date_str,
               'Hora':hour_str,
               'Producto': product_name,
               'Cantidad': quantity_sold,
               'Precio por unidad': price_per_unit,
               'Total Venta': (total_venta)}
    dataframe = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)
    st.success('Venta ingresada correctamente')
    save_sales_data(dataframe)
    return dataframe


def add_expense(dataframe, amount, reason):
    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d")
    hour_str = current_datetime.strftime("%H:%M:%S")
    new_row = {'Fecha':date_str,
               'Hora':hour_str,
               'Cantidad': amount,
               'Motivo': reason,}
    dataframe = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)
    st.success('Gasto ingresado correctamente!')
    save_expenses_data(dataframe)
    return dataframe

# def edit_sale(dataframe):
#     st.subheader('Edit Sales Data')
#     index = st.number_input('Enter index of sale to edit:', min_value=0, max_value=len(dataframe)-1, value=0)
#     if st.button('Edit Sale'):
#         product_name = st.text_input('Product Name', value=dataframe.loc[index, 'Product Name'])
#         quantity_sold = st.number_input('Quantity Sold', min_value=1, value=dataframe.loc[index, 'Quantity Sold'])
#         price_per_unit = st.number_input('Price Per Unit', min_value=0.01, format="%.2f",
#                                          value=dataframe.loc[index, 'Price Per Unit'])
#         dataframe.loc[index] = [product_name, quantity_sold, price_per_unit]
#         st.success('Sale updated successfully!')

def save_sales_data(dataframe):
    dataframe.to_csv('sales_data.csv', index=False)

def save_expenses_data(dataframe):
    dataframe.to_csv('expenditures.csv', index=False)
    
if __name__ == '__main__':
    main()
