import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re
import base64
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go

# st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.set_page_config(layout = 'wide', page_title="RTW",page_icon= '')
st.set_option('deprecation.showPyplotGlobalUse', False)

col1, col2, col3, = st.columns([0.6, 1, 0.5])
# col2.header("RIGHT TO WORK STATUS")

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


# for name, group in duplicate_rows.groupby('Names'):
#     unique_mhr_numbers = group['MHR_REF'].nunique()
#     if unique_mhr_numbers > 1:
#         group

v1, v2, v3, v4, v5 = st.columns([1, 1, 1, 1, 1])
col1, col2, col3, = st.columns([0.6, 1, 0.5])
with col2:
    st.caption('Hover on the symbol - (?) to understand the metric')
with v1:
    st.metric('Number of Practices',practices,)
with v2:
    st.metric('Total Number of Staff ', len(RTW_Data), help = 'Note that duplicate names exist in the dataset')
with v3:
    st.metric('Duplicate Names',dup)
with v4:
    st.metric('Entries with diff MHRs',dup2, help = 'These are employees with 2 different MHR Numbers')
with v5:
    st.metric('Employees Without RTW',nope, help = 'NOTE: Some of these employees are leavers')
st.write('---')
# st.write('**Generate and Download Dataset Reports for Follow-up**')
reports = ['Hold','Initial List','For iTrent','No RTW','Duplicate Names','Employees with Diff MHR Numbers', "Upload Birth Cert.", 'Already Uploaded','No Records']


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



col1, col2, = st.columns([1, 1])
co1, co2, co3, co4 = st.columns([1,0.55, 0.55,1])
def dodi():
    with co1:
        main()
    with co2:
        download()

with col1:
    repo = st.selectbox('Select a Report to Generate', reports)

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
    
    






df = duplicate_rows[['Names', 'Practice', 'MHR_REF', 'Comment']]














st.metric('Requiring Sharecode Check',req1, help = 'Employees with foreign passports -Unverified for Work')
st.metric("Employees With no Records",rec1, help = "They dont have documents - Some of these employees are leavers")














 









ncol1, ncol2, ncol3, = st.columns([0.6, 1, 0.5])

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
        st.write("**Search and Filter Data**")

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

    # if __name__ == "__main__":
    main()



# st.text(RTW_Data.columns)

# st.text(RTW_Data['Comment'].unique())
# st.text(RTW_Data['Comment'].nunique())
# st.text(RTW_Data['Comment_Final'].nunique())


local_areas = no['Practice'].value_counts().to_dict()
wordcloud = WordCloud(width=800, height=400, background_color='white',prefer_horizontal=1, scale=2)#.generate_from_frequencies(local_areas)

wordcloud.generate_from_frequencies(local_areas)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Turn off axis
# plt.title('No Right to Work Hotspots', fontsize=20, pad=20)  # Add title
plt.tight_layout(pad=0)  # Ensure tight layout
st.subheader('**No Right to Work Hotspots**')
# wordcloud_plot = create_wordcloud(text)
st.pyplot()


# no


C_Count = no['Practice'].value_counts().reset_index().rename(columns={'count': 'No RTW_Count'})
C_Count = C_Count.head(15)

fig = px.bar(C_Count,y='Practice', x='No RTW_Count', title = '', width=800, height=700)
fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries", categoryorder = 'total descending')
fig.update_layout(yaxis=dict(autorange="reversed"))
fig.update_traces(marker_color=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b',
                                '#ed7953', '#fb9f3a', '#fdca26', '#f0f921', '#b7e0a5', '#6fcae4',
                                '#c2c2c2', '#898989', '#5d5d5d'], showlegend=False)
                
st.subheader('Top 15 Right to Work Defaults')
st.plotly_chart(fig, use_container_width=True)