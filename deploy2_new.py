import pickle
import streamlit as st
 
# loading the trained model
pickle_in = open('classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)

@st.cache()

# defining the function which will make the prediction using the data which the user inputs 
def prediction(Customer_rating, Warehouse_block, Gender, Product_importance, Discount_offered, Weight_in_gms, Mode_of_Shipment, Customer_care_calls, Cost_of_the_Product, Prior_purchases):

    Warehouse_block_dict = {"A" : 0, "B" : 0, "C" : 0, "D" : 0, "F" :0 }

    for x,y in Warehouse_block_dict.items():
      if x == Warehouse_block :
          Warehouse_block_dict[x] = 1
      else :
         Warehouse_block_dict[x] = 0



    Gender_dict = {"G" : 0 }

    if 'F' == Gender :
        Gender_dict["G"] = 0
    else :
        Gender_dict["G"] = 1



    Product_importance_dict = {"low" : 0, "medium" : 0, "high" :0 } 

    for x,y in Product_importance_dict.items():
      if x == Product_importance :
         Product_importance_dict[x] = 1
      else :
         Product_importance_dict[x] = 0

 


    Mode_of_Shipment_dict = {"Flight" : 0, "Ship" : 0, "Road" : 0}

    for x,y in Mode_of_Shipment_dict.items():
        if x == Mode_of_Shipment :
          Mode_of_Shipment_dict[x] = 1
        else :
          Mode_of_Shipment_dict[x] = 0

  # Making predictions 
    prediction = classifier.predict(
       [[Customer_care_calls,Customer_rating,Cost_of_the_Product,
         Prior_purchases,Gender_dict["G"],Discount_offered,Weight_in_gms,
         Warehouse_block_dict["A"],Warehouse_block_dict["B"],Warehouse_block_dict["C"],
         Warehouse_block_dict["D"],Warehouse_block_dict["F"],
         Mode_of_Shipment_dict["Flight"],Mode_of_Shipment_dict["Road"],Mode_of_Shipment_dict["Ship"],
         Product_importance_dict["high"],Product_importance_dict["low"],Product_importance_dict["medium"]]])


     
    if prediction == 0:
        pred = 'Will Reach on Time'
    else:
        pred = 'Will Not Reach On Time'
    return pred


# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit Time Prediction ML App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    Customer_rating = st.selectbox("Insert_Ratings",("1","2","3","4","5"),key="1")
    Warehouse_block = st.selectbox("Insert_Warehouse_Block",("A","B","C","D","F"),key="1")
    Gender = st.selectbox("Insert_Gender" ,("F","M"))
    Product_importance = st.selectbox("Insert_Product_Importance",("low","medium","high"),key="1")
    Discount_offered = st.slider("Insert_Discount_offered_percentage ",1,100)
    Weight_in_gms = st.slider("Insert_Weight_in_gms ",50,10000)
    Mode_of_Shipment = st.selectbox("Insert_Mode_of_Shipment",("Flight","Ship","Road"),key="1")
    Customer_care_calls = st.number_input("Insert_Customer_Calls ",1)
    Cost_of_the_Product = st.slider("Insert_Cost_of_the_Product_USD ",10,500)
    Prior_purchases = st.number_input("Insert_Prior_purchases ",1)
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"):
        
        
        result = prediction(Customer_rating, Warehouse_block, Gender, Product_importance, Discount_offered, Weight_in_gms, Mode_of_Shipment, Customer_care_calls, Cost_of_the_Product, Prior_purchases) 
        st.success('Shipment {}'.format(result))
        print(result)
     
if __name__=='__main__': 
    main()
