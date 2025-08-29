import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import requests


st.set_page_config(page_title="InfoPulse", layout="wide")


page = st.sidebar.radio("📌 Navigation", ["Home", "Analysis Report", "About Us","Chat with Ai"])


if page == "Home":
    st.title("🏠 Welcome to InfoPulse")
    st.write("""
    InfoPulse is your **data exploration and visualization assistant**.  
    Upload your CSV file and instantly explore:
    - 📊 Data summary  
    - 🔍 Correlation heatmaps  
    - 📈 Visualizations (Scatter, Box, Bar, Heatmap)  
     
    
    Navigate to the **Analysis Report** tab from the sidebar to start exploring your dataset.
    """)
    st.success("Go to the 'Analysis Report' page from the sidebar to get started!")


elif page == "About Us":
    st.title("ℹ️ About Us")
    st.write("""
    This software was built to help **students, researchers, and analysts** 
    quickly analyze and visualize datasets without needing to write code.  

    ✨ Features:
    - Simple CSV upload  
    - Automatic summary statistics  
    - Interactive plots  
    - Easy correlation heatmaps  

    👨‍💻 Developed by: *Ganesha......*  
    """)


elif page == "Analysis Report":
    st.title("📊 Analysis Report")
    st.write("Upload your dataset to begin analysis.")

    file = st.file_uploader(label="Upload here (CSV only)", type=".csv",key="analysis")

    if file is not None:
        if st.button("Read Data"):
            st.write("This is read configuration")
            with st.spinner("Analyzing your data..."):
                 
                df = pd.read_csv(file)
                df = df.dropna(how='all')

            st.write("Here is brief data extraction on it")
            st.dataframe(df.head())
            st.session_state.df = df
            st.success("✅ Data read successfully!")

    
    if "df" in st.session_state:
        choice = st.selectbox("Do you want to explore the data?", ["yes", "no"], key="choice")

        if st.button("Submit"):
            st.session_state.submitted = True

        if st.session_state.get("submitted", False):
            if st.session_state.choice == "yes":
                df = st.session_state.df

                st.subheader("Here is data summary")
                st.dataframe(df.describe())

                st.write("Here is the brief info of the data and NaN values present in it")
                info_df = pd.DataFrame({
                    "Column": df.columns,
                    "Non-Null Count": df.notnull().sum().values,
                    "Null Count": df.isnull().sum().values,
                    "Dtype": df.dtypes.values
                })
                st.dataframe(info_df)
                st.write(f"There are {df.shape[0]*df.shape[1]} data points \n ({df.shape[0]} rows × {df.shape[1]} columns)")

                prefer = st.selectbox(
                    "Do you want to see correlation matrix of this data",
                    ["yes", "no"],
                    key="prefer"
                )

                if prefer == "yes":
                    st.subheader("Correlation between columns")
                    # st.dataframe(df.corr(numeric_only=True))

                    plt.figure(figsize=(10, 6))
                    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
                    st.pyplot(plt)

                    st.info("In this heatmap:\n- Darker color → Strong correlation\n- Lighter color → Weak correlation")

                   
                   

                        


                    

                # Visualization block
                st.subheader("Visualization of features")
                choice_viz = st.selectbox(
                    "Choose visualization type", 
                    ["Scatter Plot", "Box Plot", "Bar Plot", "Heat Map"],
                    key="choice_viz"
                )

                columns = st.multiselect("Select columns for visualization", df.columns.tolist())
                st.warning("⚠ For Scatter Plot select 3 cols (x,y,hue). For Box/Bar select 1+. For Heat Map select 3.")

                if st.button("Generate Plot"):
                    if choice_viz == "Scatter Plot" and len(columns) == 3:
                        plt.figure(figsize=(8, 6))
                        sns.scatterplot(data=df, x=columns[0], y=columns[1], hue=columns[2])
                        plt.title(f'Scatter Plot of {columns[0]} vs {columns[1]}')
                        st.pyplot(plt)

                    elif choice_viz == "Bar Plot" and len(columns) >= 1:
                        plt.figure(figsize=(8, 6))
                        df[columns].value_counts().plot(kind='bar')
                        plt.title(f'Bar Plot of {", ".join(columns)}')
                        st.pyplot(plt)

                    elif choice_viz == "Box Plot" and len(columns) >= 1:
                        plt.figure(figsize=(8, 6))
                        sns.boxplot(data=df[columns])
                        plt.title(f'Box Plot of {", ".join(columns)}')
                        st.pyplot(plt)

                    elif choice_viz == "Heat Map" and len(columns) >= 3:
                        corelation = pd.pivot_table(index=columns[0], columns=columns[1], values=columns[2], data=df)
                        plt.figure(figsize=(10, 6))
                        sns.heatmap(corelation, annot=True, cmap='magma', mask=corelation.isnull())
                        plt.title(f"Relation with respect to {columns[2]}")
                        st.pyplot(plt)
elif page=="Chat with Ai":



 st.title("🤖 FILE ANALYSIS")
 if "csv_file" not in st.session_state:
     st.session_state.csv_data=None
 if "csv_name" not in st.session_state:
     st.session_state.csv_name=""    


 if "message" not in st.session_state:
    st.session_state.message = []

 uploaded_file=st.file_uploader("upload csv file for analysis",type=["csv"],key="uploaded")
 if uploaded_file:
  st.session_state.csv_data=pd.read_csv(uploaded_file)
  st.session_state.csv_name=uploaded_file.name
  st.success(f"File '{st.session_state.csv_name}' uploaded successfully!")
 for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


 prompt = st.chat_input("Analyze it", accept_file=False)

 if prompt:
    user_input=prompt
    with st.chat_message("human"):
        st.markdown(user_input)
    st.session_state.message.append({"role": "human", "content": user_input})
    if st.session_state.csv_data is not None:
        df2=st.session_state.csv_data
        df_summary=df2.describe().to_string()
        df_preview=df2.sample(min(20,len(df2))).to_string()
        ai_input=f"data summary is {df_summary}\n data preview is {df_preview}\n now answer the question based on this data {user_input}"
    else:   
        ai_input=user_input               
            
    with st.spinner("Getting answers..."):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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"
        }
        data = {
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [{"role": "system", "content": "you are a data analysis expert. You help users analyze their data files and answer questions based on the data provided."}, {"role": "user", "content": ai_input}]
        }

        for attempt in range(5):
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 429:
                st.warning("Rate limited, retrying in 2 seconds...")
                
            else:
                break

        # Process API response
        if response.status_code == 200:
            try:
                answer = response.json()
                ai_response = answer['choices'][0]['message']['content']
            except (KeyError, IndexError):
                ai_response = "Unexpected response format."
        else:
            ai_response = f"API request failed with status code {response.status_code}"

        # Show AI message
        with st.chat_message("ai"):
            st.markdown(ai_response)
        st.session_state.message.append({"role": "ai", "content": ai_response})
    
 
   


                            










                    
                

            





  



            
                             
                      

                 
            
            
            
            



            


 

