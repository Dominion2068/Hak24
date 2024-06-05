import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import platform
import plotly
import re
import base64
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go


# st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(layout = 'wide', page_title="RTW",page_icon= '')
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.set_option('deprecation.showPyplotGlobalUse', False)

col1, col2, col3, = st.columns([0.6, 1, 0.5])
col2.header("RIGHT TO WORK STATUS")
st.write('---')

expand = st.radio(label = (f"**Click to Explore**"), options = ['Hold',
                                                            "About",
                                                            "Updates",
                                                            'Current Status',
                                                            'Reports, Search and Filter'
                                                            ])
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.write('---')

ol1, ol2, ol3, = st.columns([0.4, 1, 0.4])
if expand == "About":
    with ol2:
        st.write('''This application assesses right-to-work data for the organization and enables 
        the generation and download of various reports to capture the current status, facilitating 
        follow-ups and necessary actions to correct any anomalies. In addition to right-to-work reports, 
        you can generate and download other reports related to the proper identity management of staff members. 
        The application also includes visualizations that offer deeper insights into the current situation.
        The technology used for this application are:''')

        # Display Python version
        python_version = f"1. Python(Programming Language) Version:- {platform.python_version()}"

        # Display library versions
        pandas_version = f"2. Pandas(Data Manipulation Library) Version:- {pd.__version__}"
        numpy_version = f"3. Numpy(Numerical Python Library) Version:- {np.__version__}"
        streamlit_version = f"4. Streamlit(Web Application Library) Version:- {st.__version__}"
        plotly_version = f"5. Plotly(Data Visualization Library) Version:- {plotly.__version__}"

        # Print the versions
        st.write(python_version)
        st.write(pandas_version)
        st.write(numpy_version)
        st.write(streamlit_version)
        st.write(plotly_version)
        


RTW_Data = pd.read_excel('RTW.xlsx', sheet_name="Passport Details")
dropped = RTW_Data[['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14']]
RTW_Data = RTW_Data.drop(dropped, axis=1)
RTW_Data['Comment'] = RTW_Data['Comment'].replace({'Head office': 'Head Office', 
                                                'Birth certificate': 'Birth Certificate',
                                                'ILR Status ': 'ILR Status',
                                                'Birth Certificate ': 'Birth Certificate',
                                                'Incomplete RTW ': 'Incomplete RTW',
                                                'No RTW -Leaver': 'No RTW - Leaver',
                                                'Blurry Passport details': 'Blurry Passport Details'})

RTW_Data['Comment'] = RTW_Data['Comment'].fillna('RTW-OKAY').astype(str)
RTW_Data['Names'] = RTW_Data['Name'] + ' ' + RTW_Data['Surname']

practices = (RTW_Data['Practice'].nunique())
# dup = RTW_Data[(RTW_Data['Comment'] == 'Duplicate')]
duplicate_rows = RTW_Data[RTW_Data.duplicated(subset=['Names'], keep=False)]
duplicate_rows.sort_values(by='Names', inplace=True)
# duplicate_rows


dup = duplicate_rows[['Names']].nunique()
df = duplicate_rows.groupby('Names').filter(lambda x: x['MHR_REF'].nunique() > 1)
df.sort_values(by='Names', inplace=True)
# result_df
dup2 = df[['Names']].nunique()

no = RTW_Data[(RTW_Data['Comment'] == 'No RTW') | (RTW_Data['Comment'] == 'No RTW - Leaver') ]
nope = len(no)

req = RTW_Data[(RTW_Data['Comment'] == 'Sharecode Check Required')]
# req
req1 = len(req)

rec = RTW_Data[(RTW_Data['Comment'] == 'No Records')]
# rec
rec1 = len(rec)

blurry = RTW_Data[(RTW_Data['Comment'] == 'Blurry Passport Details')]

ILR = RTW_Data[(RTW_Data['Comment'] == 'ILR Status')]
ILR1 = len(ILR)

hq = RTW_Data[(RTW_Data['Comment'] == 'Head Office')]
hq1 = len(hq)
# ILR
# blurry
yeah = RTW_Data[(RTW_Data['Comment'] == 'Birth Certificate')]
BRT = len(yeah)

limt = RTW_Data[(RTW_Data['Comment'] == 'Limited RTW Status')]
LIM = len(limt)

incom = RTW_Data[(RTW_Data['Comment'] == 'Incomplete RTW')]
#LIM = len(limt)

# for name, group in duplicate_rows.groupby('Names'):
#     unique_mhr_numbers = group['MHR_REF'].nunique()
#     if unique_mhr_numbers > 1:
#         group
if expand == 'Current Status':
    v1, v2, v3, v4, v5 = st.columns([1, 1, 1, 1, 1])
    col1, col2, col3, = st.columns([0.6, 1, 0.5])
    with col2:
        st.caption('Hover on the symbol - (?) to understand the metric')
    with v1:
        st.metric('Number of Practices',practices, help = '....as contained in the list provided')
    with v2:
        st.metric('Total Number of Staff ', len(RTW_Data), help = 'Note that duplicate names (Employee whose names were repeated more than once) exist in the dataset')
    with v3:
        st.metric('Duplicate Names',dup,  help = 'These are employees with more than one entry within or outside the same Practice')
    with v4:
        st.metric('Entries with diff MHRs',dup2, help = 'These are employees with 2 different MHR Numbers')
    with v5:
        st.metric('Employees Without RTW',nope, help = 'NOTE: Some of these employees are leavers')
    # st.write('---')

    vg1, vg2 = st.columns([1, 1])
    
    with vg1:
        all_Count = RTW_Data['Comment'].value_counts().reset_index().rename(columns={'count': 'Incedence_Count', 'Comment': 'Findings'})
        

        fig = px.bar(all_Count,y='Incedence_Count', x='Findings', title = '', width=800, height=700)
        fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries", categoryorder = 'total descending')
        fig.update_layout(title='General Findings', height=500)
        fig.update_traces(marker_color=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b',
                                        '#ed7953', '#fb9f3a', '#fdca26', '#f0f921', '#b7e0a5', '#6fcae4',
                                        '#c2c2c2', 'olivedrab', 'orangered','mediumslateblue', 'mediumaquamarine',
                                        'lightsteelblue','saddlebrown', 'slategrey'], showlegend=False)
                        
        # st.subheader("General Findings")
        st.plotly_chart(fig, use_container_width=True)

    
    with vg2:
        # Assuming RTW_Data is a DataFrame with a 'Comment' column
        C_Count = RTW_Data[(RTW_Data['Comment'] == 'Duplicate') | (RTW_Data['Comment'] == 'No RTW') | 
                        (RTW_Data['Comment'] == 'Sharecode Check Required') | 
                        (RTW_Data['Comment'] == 'No Records') | (RTW_Data['Comment'] == 'Blurry Passport Details') |
                        (RTW_Data['Comment'] == 'Limited RTW Status') | (RTW_Data['Comment'] == 'No RTW - Leaver')
                        
                        ]
        # Identify duplicated names
        duplicated_names = RTW_Data[RTW_Data.duplicated(subset='Names', keep=False)]

        # Count the number of duplicate names
        duplicate_count = len(duplicated_names['Names'].unique())
        # st.write(duplicate_count)

        # Create a DataFrame for the duplicate count
        duplicate_count_df = pd.DataFrame({'Category': ['Duplicates'], 'Count': [duplicate_count]})

        # Filtered DataFrame based on specified comment conditions
        comments_of_interest = ['No RTW', 'Sharecode Check Required', 'No Records', 
                                'Blurry Passport Details', 'Limited RTW Status', 
                                'No RTW - Leaver', 'Valid RTW']

        filtered_comments = RTW_Data[RTW_Data['Comment'].isin(comments_of_interest)]

        # Count the occurrences of each specified comment
        comment_counts = filtered_comments['Comment'].value_counts().reset_index()
        comment_counts.columns = ['Category', 'Count']

        # Combine the counts into a single DataFrame
        combined_counts = pd.concat([comment_counts, duplicate_count_df]).reset_index(drop=True)

        labels = combined_counts['Category'].tolist()
        values = combined_counts['Count'].tolist()

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.1, 0.1, 0.2, 0.1], textinfo='label+percent')])
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.write('**Focussing on the Issues Only**')
        # Generate HTML code to move the chart up
        st.plotly_chart(fig, use_container_width=True)

    # labels = C_Count1['Comment'].tolist()
    # values = C_Count1['Current-Status%'].tolist()
    # fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.1, 0.1, 0.2, 0.1],extinfo='label+percent')])
    # fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
    # # Generate HTML code to move the chart up
    # st.plotly_chart(fig, use_container_width=True)
    st.write('---')



    vaga, vagb, vagc = st.columns([1, 1, 1])
    with vaga:
        st.metric('Requiring Sharecode Check',req1, help = 'Employees with non-British passports - Unverified for Work')
    with vagb:
        st.metric("Employees With no Records",rec1, help = "They dont have documents in the required folders - Some of these employees are leavers")
    with vagc:
        st.metric("Employees With Indefinite Leave to Remain",ILR1, help = "Some of these employees did not present their passports")
    # with vagd:
    #     st.metric("Head Office Employees",hq1)

    st.write('---')
    vga, vgb = st.columns([1, 0.6])

    with vgb:
        C_Count = no['Practice'].value_counts().reset_index().rename(columns={'count': 'No RTW_Count'})
        C_Count = C_Count.head(20)

        fig = px.bar(C_Count,y='Practice', x='No RTW_Count', title = '', width=800, height=850)
        fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries", categoryorder = 'total descending')
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_traces(marker_color=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b',
                                        '#ed7953', '#fb9f3a', '#fdca26', '#f0f921', '#b7e0a5', '#6fcae4',
                                        '#c2c2c2', 'olivedrab', 'orangered','mediumslateblue', 'mediumaquamarine',
                                        'lightsteelblue','saddlebrown', 'slategrey'], showlegend=False)
                        
        st.write("**Top 20 Right-to-Work Defaults**")
        st.plotly_chart(fig, use_container_width=True)
        

    with vga:
        local_areas = no['Practice'].value_counts().to_dict()
        wordcloud = WordCloud(width=800, height=800, background_color='white',prefer_horizontal=1, scale=2)#.generate_from_frequencies(local_areas)

        wordcloud.generate_from_frequencies(local_areas)

        # Display the word cloud using matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # Turn off axis
        # plt.title('No Right to Work Hotspots', fontsize=20, pad=20)  # Add title
        plt.tight_layout(pad=0)  # Ensure tight layout
        st.write('''**'No-Right-to-Work' Hotspots**''')
        # wordcloud_plot = create_wordcloud(text)
        st.pyplot()







if expand == 'Reports, Search and Filter':
    #with v5:
    # st.write('**Generate and Download Dataset Reports for Follow-up**')
    reports = ['For iTrent Upload','No RTW','Duplicate Names','Employees with Diff MHR Numbers', 
               "Birth Cert. List", 'Already Uploaded','No Records','Blurry Passports','HQ No Records',
               'ILR Status', 'Sharecode Check Required', 'Limited RTW Status']

    st.write(' ')
    fileName_csv = ''

    def download():
        @st.cache_data
        def convert_df(result_df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode("utf-8")

        csv = convert_df(df)

        st.download_button(
            label="Download as CSV File",
            data=csv,
            file_name= fileName_csv,
            mime="text/csv",
        )


    # Function to create a downloadable link for Excel file
    def download_excel(df, filename):
        # Create a BytesIO buffer for the Excel file
        excel_buffer = BytesIO()
        
        # Use pandas to write the DataFrame to the BytesIO buffer as an Excel file
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        
        # Retrieve the Excel file from the buffer
        excel_data = excel_buffer.getvalue()
        
        # Encode the Excel data in base64
        b64 = base64.b64encode(excel_data).decode()
        
        # Generate download link
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Download Excel file</a>'
        return href

    # Main Streamlit app
    def main():
        # Add a download button
        button = st.button("Download as Excel File")
        if button:
            st.markdown(download_excel(df, fileName), unsafe_allow_html=True)



    col1, col2, = st.columns([1, 0.8])
    co1, co2, co3, co4 = st.columns([1,0.55, 0.55,1])
    def dodi():
        with co1:
            main()
        with co2:
            download()

    with col1:
        st.metric('Employees using Birth Cert. as RTW',BRT, help = 'NOTE: They are required to have evidence of NI')
        st.write('')
        repo = st.selectbox('Select a Report to Generate and Download', reports)

        if repo == 'Employees with Diff MHR Numbers':
            df = df[['Names', 'Practice', 'MHR_REF', 'Comment']]
            df
            fileName_csv = 'MHR_Conflicts.csv'
            fileName = 'MHR_Conflicts'
            dodi()


        if repo == 'Duplicate Names':
            duplicate_rows = duplicate_rows[['Names', 'Practice', 'MHR_REF', 'Comment']]
            df = duplicate_rows
            duplicate_rows
            fileName_csv = 'Duplicate names.csv'
            fileName = 'Duplicate names'
            dodi()

        if repo == 'No Records':
            rec = rec[['Names', 'Practice', 'MHR_REF', 'Comment']]
            df = rec
            rec
            fileName_csv = 'No Records.csv'
            fileName = 'No Records'
            dodi()
        
        if repo == 'For iTrent Upload':
            RTW_Data['ISSUE_DATE'] = pd.to_datetime(RTW_Data['ISSUE_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y%m%d')
            RTW_Data['EXPIRY_DATE'] = pd.to_datetime(RTW_Data['EXPIRY_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y%m%d')
            yeah = RTW_Data[(RTW_Data['Comment'] == 'RTW-OKAY')]
            rec = yeah[['MHR_REF', 'ISSUE_DATE', 'PASSPORT_NO','EXPIRY_DATE', 'COUNTRY']]
            df = rec
            rec
            fileName_csv = 'For iTrent Upload.csv'
            fileName = 'For iTrent Upload'
            dodi()

        if repo == 'Birth Cert. List':
            yeah = RTW_Data[(RTW_Data['Comment'] == 'Birth Certificate')]
            rec = yeah[['Names', 'Practice', 'MHR_REF']]
            df = rec
            rec
            fileName_csv = 'Upload Birth Certificate.csv'
            fileName = 'Upload Birth Certificate'
            dodi()

        if repo == 'Already Uploaded':
            yeah = RTW_Data[(RTW_Data['Comment'] == 'RTW Uploaded')]
            rec = yeah[['Names', 'Practice', 'MHR_REF']]
            df = rec
            rec
            fileName_csv = 'Already Uploaded.csv'
            fileName = 'Already Uploaded'
            dodi()
        
        if repo == 'No RTW':
            yeah = RTW_Data[(RTW_Data['Comment'] == 'No RTW') | (RTW_Data['Comment'] == 'No RTW - Leaver')]
            rec = yeah[['Names', 'Practice', 'MHR_REF']]
            df = rec
            rec
            fileName_csv = 'No RTW.csv'
            fileName = 'No RTW'
            dodi()
        
        if repo =='Blurry Passports':
            df = blurry
            blurry
            fileName_csv = 'Blurry Passport List.csv'
            fileName = 'Blurry Passport List'
            dodi()

        if repo =='HQ No Records':
            HQ = RTW_Data[(RTW_Data['Comment'] == 'HQ No Records')]
            HQ = HQ[['Names', 'Practice', 'MHR_REF']]
            df = HQ
            HQ
            fileName_csv = 'HQ No Records.csv'
            fileName = 'HQ No Records'
            dodi()
        
        if repo =='ILR Status':
            ILR = RTW_Data[(RTW_Data['Comment'] == 'ILR Status')]
            ILR = ILR[['Names', 'Practice', 'MHR_REF', 'PASSPORT_NO']]
            df = ILR
            ILR
            fileName_csv = 'ILR Status.csv'
            fileName = 'ILR Status'
            dodi()
        if repo =='Sharecode Check Required':
            share = RTW_Data[(RTW_Data['Comment'] == 'Sharecode Check Required')]
            share = share[['Names', 'Practice', 'MHR_REF', 'COUNTRY']]
            df = share
            share
            fileName_csv = 'Sharecode Check.csv'
            fileName = 'Sharecode Check'
            dodi()

        if repo =='Limited RTW Status':
            limited = RTW_Data[(RTW_Data['Comment'] == 'Limited RTW Status')]
            limited = limited[['Names', 'Practice', 'MHR_REF', 'COUNTRY']]
            df = limited
            limited
            fileName_csv = 'Limited_RTW.csv'
            fileName = 'Limited_RTW'
            dodi()

    st.write('---')


    with col2:
        st.metric('Employees with Limited RTW Status',LIM, help = 'NOTE: Their RTW has expiry status')
        st.write('')
        st.write('**Summary**')
        if repo == 'For iTrent Upload':
            st.write('Employees with Correct Right-to-Work Documents')
            yeah = RTW_Data[(RTW_Data['Comment'] == 'RTW-OKAY')]
            df = yeah[['MHR_REF', 'ISSUE_DATE', 'PASSPORT_NO','EXPIRY_DATE', 'COUNTRY', 'Practice']]
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        elif repo == 'Employees with Diff MHR Numbers':
            st.write('Employees with more than one MHR Numbers')
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        elif repo == 'Already Uploaded':
            st.write('Employees whose Docs are Already Uploded on iTrent')
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        elif repo == 'Birth Cert. List':
            st.write('Employees whose RTW Documents are Birth Certificates')
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        elif repo == 'HQ No Records':
            st.write('This is the Head Office Employees without Records')
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        elif repo == 'Sharecode Check Required':
            st.write('Employees who require sharecode check')
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        elif repo =='Limited RTW Status':
            st.write('Employees with Limited RTW Status')
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        else:
            st.write('Employees with',repo)
            df = df['Practice'].value_counts().reset_index().rename(columns={'count': 'Number_of_Employees'})
            df
        

        
        











    # df = duplicate_rows[['Names', 'Practice', 'MHR_REF', 'Comment']]


    st.caption("You can search by typing Names, MHR Numbers and Practices fully or partially in the space provided")
    ncol1, ncol2 = st.columns([0.6, 1])

    with ncol1:
        #Convert date columns to datetime and format them
        df = RTW_Data
        df['ISSUE_DATE'] = pd.to_datetime(df['ISSUE_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
        df['EXPIRY_DATE'] = pd.to_datetime(df['EXPIRY_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')

        # Function to filter DataFrame based on search query
        def filter_data(search_query):
            if search_query.isdigit() and len(search_query) >= 4:
                # Search by last four digits of MHR number
                filtered_df = RTW_Data[RTW_Data['MHR_REF'].str.endswith(search_query)]
            else:
                # Search by MHR_REF or any part of Name
                filtered_df = RTW_Data[
                    (RTW_Data['MHR_REF'].str.contains(search_query, case=False)) |
                    (RTW_Data['Names'].str.contains(search_query, case=False))
                ]
            
            return filtered_df

        # JavaScript code to enable dynamic suggestions
        autocomplete_script = """
        <script>
        var input = document.getElementById("search_input");
        input.addEventListener("input", function() {
            var value = input.value.toLowerCase();
            var options = %s;
            var filteredOptions = [];
            options.forEach(function(option) {
                if (option.toLowerCase().startsWith(value)) {
                    filteredOptions.push(option);
                }
            });
            input.setAttribute("list", "suggestions");
            var datalist = document.createElement("datalist");
            datalist.id = "suggestions";
            filteredOptions.forEach(function(option) {
                var optionElem = document.createElement("option");
                optionElem.value = option;
                datalist.appendChild(optionElem);
            });
            var existingDatalist = document.getElementById("suggestions");
            if (existingDatalist) {
                existingDatalist.parentNode.removeChild(existingDatalist);
            }
            input.parentNode.appendChild(datalist);
        });
        </script>
        """

        # Main Streamlit app

        # Main Streamlit app
        def main():
            

            # Add autocomplete JavaScript to the Streamlit app
            st.markdown(autocomplete_script % RTW_Data['MHR_REF'].astype(str).tolist(), unsafe_allow_html=True)

            # Search field with dynamic autocomplete
            search_query = st.text_input("Search by MHR_REF or Name:", key='search_input4@', help="Type to search...")

            # Filter data based on search query
            if search_query:
                filtered_df = filter_data(search_query)
                st.write("Filtered Results:")
                if not filtered_df.empty:
                    # Display filtered results including names
                    for index, row in filtered_df.iterrows():
                        row_dict = row.fillna("None").to_dict()
            
                        # Construct the information string with single line spacing
                        info_string = (
                            f"- Name: {row_dict['Names']} \n"
                            f"- MHR_Number: {row_dict['MHR_REF']} \n"
                            f"- Practice_Name: {row_dict['Practice']} \n"
                            f"- Status: {row_dict['Comment']} \n"
                            f"- Passport Number: {row_dict['PASSPORT_NO']} \n"
                            f"- Passport Issue Date: {row_dict['ISSUE_DATE']} \n"
                            f"- Passport Expiry Date: {row_dict['EXPIRY_DATE']} \n"
                            f"- Country: {row_dict['COUNTRY']}"
                        )

                        # Write the information string with single line spacing
                        st.write(info_string)

                else:
                    st.write("No matching records found.")
            else:
                st.write("Enter a search query to filter the data.")
        main()


    



    with ncol2:
        #Convert date columns to datetime and format them
        df = RTW_Data
        df['ISSUE_DATE'] = pd.to_datetime(df['ISSUE_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
        df['EXPIRY_DATE'] = pd.to_datetime(df['EXPIRY_DATE'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')

        # Function to filter DataFrame based on search query
        def filter_data(search_query):
            if search_query.isdigit() and len(search_query) >= 4:
                # Search by last four digits of MHR number
                filtered_df = RTW_Data[RTW_Data['MHR_REF'].str.endswith(search_query)]
            else:
                # Search by MHR_REF or any part of Name
                filtered_df = RTW_Data[
                    (RTW_Data['Practice'].str.contains(search_query, case=False))
                ]
            
            return filtered_df

        # JavaScript code to enable dynamic suggestions
        autocomplete_script = """
        <script>
        var input = document.getElementById("search_input");
        input.addEventListener("input", function() {
            var value = input.value.toLowerCase();
            var options = %s;
            var filteredOptions = [];
            options.forEach(function(option) {
                if (option.toLowerCase().startsWith(value)) {
                    filteredOptions.push(option);
                }
            });
            input.setAttribute("list", "suggestions");
            var datalist = document.createElement("datalist");
            datalist.id = "suggestions";
            filteredOptions.forEach(function(option) {
                var optionElem = document.createElement("option");
                optionElem.value = option;
                datalist.appendChild(optionElem);
            });
            var existingDatalist = document.getElementById("suggestions");
            if (existingDatalist) {
                existingDatalist.parentNode.removeChild(existingDatalist);
            }
            input.parentNode.appendChild(datalist);
        });
        </script>
        """

        # Main Streamlit app

        # Main Streamlit app
        def main():

            # Add autocomplete JavaScript to the Streamlit app
            st.markdown(autocomplete_script % RTW_Data['Practice'].astype(str).tolist(), unsafe_allow_html=True)

            # Search field with dynamic autocomplete
            search_query = st.text_input("Search by Names of Practice:", key='search_input4@q&', help="Type to search...")

            # Filter data based on search query
            if search_query:
                filtered_df = filter_data(search_query)
                st.write("Filtered Results:")
                if not filtered_df.empty:
                    # Display filtered results including names
                    filtered_df

                else:
                    st.write("No matching records found.")
            else:
                st.write("Enter a search query to filter the data.")
        main()

if expand == "Updates":
    st.write(f'''**29th May 2024**  
            Begin daily updates of the RTW status using documents downloaded from the old HR system.  
            You may notice frequent changes, as I am discovering that some employees who previously  
            lacked RTW documentation actually have their documents stored in the old system.''')
    st.write(f'''**30th May 2024**     
            Based on the meeting I had with Aadil on the 29th of May 2024, I added 2 reports and 2 metrics. The reports are:\n'''
            f"- Employees who require sharecodes to complete their RTW and\n"
            f"- Employees with Limited RTW Status\n")
    st.write(f'''The metrics: are the number of employees using Birth Certificates as their RTW and those with   
            expiry status on their RTW. Both metrics are on the report page.  
            ''')
    st.write(f'''**5th June 2024**  
            The RTW for Head Office staff were updated. This is work in progress because some employees'  
            documents are missing and they have been captured as HQ No Records. I expect this to change soon  
            as the shared folder is updated. There is no more stand-alone report for head office however,  
            I have included the head office employees without records as a report.
             ''')


# st.text(RTW_Data.columns)

# st.text(RTW_Data['Comment'].unique())
# st.text(RTW_Data['Comment'].nunique())
# st.text(RTW_Data['Comment_Final'].nunique())











# st.text(RTW_Data['Comment'].unique())
# st.text(RTW_Data.columns)



# def convert_date_format(df, columns, new_format):
#                 for column in columns:
#                     try:
#                         df[column] = pd.to_datetime(df[column], format='%Y%m%d').dt.strftime(new_format)
#                     except ValueError:
#                         raise ValueError(f"Invalid date format in column '{column}'. Please enter dates in YYYYMMDD format.")
#                 return df

            
#             # Streamlit UI
#             st.title("Date Format Converter")

#             # Display original DataFrame
#             st.subheader("Original DataFrame:")
#             st.write(df)

#             # Select columns and new date format
#             columns_to_convert = st.multiselect("Select columns to convert:", df.columns)
#             new_date_format = st.selectbox("Select new date format:", [
#                 "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d", "%d/%m/%Y", 
#                 "%m-%d-%Y", "%Y.%m.%d", "%d.%m.%Y", "%m%d%Y", "%m-%d-%y", "%d%m%Y"
#             ])

#             # Convert and display
#             if st.button("Convert"):
#                 try:
#                     converted_df = convert_date_format(df.copy(), columns_to_convert, new_date_format)
#                     st.subheader("Converted DataFrame:")
#                     st.write(converted_df)
#                 except ValueError as e:
#                     st.error(str(e))



#st.text(RTW_Data['Comment'].unique())







# import rpy2.robjects as robjects

# try:
#     import rpy2.robjects as robjects
# except OSError as e:
#     try:
#         import os
#         import platform
#         if platform.system() == 'Windows':
#             os.environ["R_HOME"] = 'C:/Program Files/R/R-4.4.0'  # Your R version here 'R-4.0.3'
#             os.environ["PATH"] = "C:/Program Files/R/R-4.4.0/bin/x64" + ";" + os.environ["PATH"]
#         import rpy2.robjects as robjects
#     except OSError:
#         raise e


    

# r_code = st.text_area("Write R code here", height=200)

# # Button to run R code
# if st.button("Run R Code"):
#     try:
#         result = robjects.r(r_code)
#         st.write("Result:", result)
#     except Exception as e:
#         st.error(f"Error: {e}")

# st.text('joy')

