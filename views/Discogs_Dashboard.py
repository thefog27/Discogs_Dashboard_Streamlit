import re
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px




# -- Config --

def vis_time_series(category, color):
    df_time_series = df
    #df_time_series = df[df['year'] != 0]
    #df_time_series = df_time_series.sort_values('year')

    fig = px.bar(df_time_series.groupby(['year',category]).agg(countt = ('release_id' ,'count')).reset_index(), x= 'year', y='countt', color= category
                , template='plotly_dark'
                , category_orders={'year': sorted(df_time_series['year'].unique())}
                , color_discrete_sequence=color
                #text_auto='.1s'
                )
    # Chart Title
    fig.update_layout(title='Releases by year'
                    , title_font_size = 20
                    , title_x=0.0
                    )
    # Margin under Title - Top
    fig.update_layout(margin=dict(t=80))
    # Change Name and Position of Y Axes
    fig.update_yaxes(title='# releases'
                    #, tickfont=dict(size=16)
                    )
    # Change Name and Position of x Axes
    fig.update_xaxes(title= 'year'
                    , tickfont=dict(size=16)
                    )
    #Y Axis Format
    #fig.update_layout( yaxis_ticksuffix=' €')

    # Description Margin - Bottom
    fig.update_layout(margin=dict(b=70))
    #fig.show()
    st.plotly_chart(fig)
    
    st.markdown(
    """
        <div style='
            font-size:13px;
            margin-top:-20px;    
            margin-bottom:30px;  
        '>
        🛈 <strong>Note:</strong> 0 refers to an unknown release year.
        </div>
        """,
    unsafe_allow_html=True
    ) 
#vis_time_series()

def vis_distribution(category):

    df_split_genres = df.copy() #df_vis_dist.copy() #df.copy()
    df_split_styles = df.copy() #df_vis_dist.copy() #df.copy()

    df_split_genres['genres'] = df_split_genres['genres'].str.split(',')
    df_split_styles['styles'] = df_split_styles['styles'].str.split(',')

    df_split_genres = df_split_genres.explode('genres').reset_index(drop=True)
    df_split_styles = df_split_styles.explode('styles').reset_index(drop=True)

    df_split_genres['genres'] = df_split_genres['genres'].str.lstrip() #remove leading spaces
    df_split_styles['styles'] = df_split_styles['styles'].str.lstrip()


    # dataframes = {
    #     "genres": df_split_genres,
    #     "styles": df_split_styles
    # }

    if category == 'genres':

    #dc_distribution_styles = dataframes.get(category)

        df_split_genres = df_split_genres[
                 (df_split_genres['styles'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in styles_filter)) if styles_filter else df_split_genres['styles'].notna()) &
                 (df_split_genres['genres'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in genres_filter)) if genres_filter else df_split_genres['genres'].notna()) &
                #  (df_split_genres['styles'].isin(styles_filter) if styles_filter else df_split_genres['styles'].notna()) &
                #  (df_split_genres['genres'].isin(genres_filter) if genres_filter else df_split_genres['genres'].notna()) &
                # (df_split_genres['year'].isin(year_filter) if year_filter else df_split_genres['year'].notna()) &
                 ((df_split_genres['year'] >= start_jahr) & (df_split_genres['year'] <= end_jahr) if year_filter else df_split_genres['year'].notna()) &
                 (df_split_genres['label'].isin(label_filter) if label_filter else df_split_genres['label'].notna()) &
                 (df_split_genres['artist'].isin(artist_filter) if artist_filter else df_split_genres['artist'].notna()) &
                 (df_split_genres['Collection vs. Wantlist'].isin(collection_wantlist_filter) if collection_wantlist_filter else df_split_genres['Collection vs. Wantlist'].notna()) &
                 (df_split_genres['Reissue/Remaster'].isin(remaster_reissue_filter) if remaster_reissue_filter else df_split_genres['Reissue/Remaster'].notna())
                 ]
        dc_distribution_styles = df_split_genres

        fig = px.bar(dc_distribution_styles.groupby(category).agg(countt = ('release_id' ,'count')).reset_index(), y= category , x='countt', color= category,
            template='plotly_dark')
        
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})


    #elif category == 'styles':
    else:

        df_split_styles = df_split_styles[
                        (df_split_styles['styles'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in styles_filter)) if styles_filter else df_split_styles['styles'].notna()) &
                        (df_split_styles['genres'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in genres_filter)) if genres_filter else df_split_styles['genres'].notna()) &
                        # (df_split_styles['styles'].isin(styles_filter) if styles_filter else df_split_styles['styles'].notna()) &
                        # (df_split_styles['genres'].isin(genres_filter) if genres_filter else df_split_styles['genres'].notna()) &
                        # (df_split_styles['year'].isin(year_filter) if year_filter else df_split_styles['year'].notna()) &
                        # ((df['year'] >= start_jahr) & (df['year'] <= end_jahr) if year_filter else True) &
                        ((df_split_styles['year'] >= start_jahr) & (df_split_styles['year'] <= end_jahr) if year_filter else df_split_styles['year'].notna()) &
                        (df_split_styles['label'].isin(label_filter) if label_filter else df_split_styles['label'].notna()) &
                        (df_split_styles['artist'].isin(artist_filter) if artist_filter else df_split_styles['artist'].notna()) &
                        (df_split_styles['Collection vs. Wantlist'].isin(collection_wantlist_filter) if collection_wantlist_filter else df_split_styles['Collection vs. Wantlist'].notna()) &
                        (df_split_styles['Reissue/Remaster'].isin(remaster_reissue_filter) if remaster_reissue_filter else df_split_styles['Reissue/Remaster'].notna())
                        ]
        dc_distribution_styles = df_split_styles

        fig = px.bar(dc_distribution_styles.groupby(category).agg(countt = ('release_id' ,'count')).reset_index(), x= category , y='countt', color= category,
                template='plotly_dark')
        
        fig.update_layout(xaxis={'categoryorder': 'total descending'})

        fig.update_xaxes(rangeslider_visible=True)

    # Chart Title
    fig.update_layout(title=f'Releases by {category}'
                    , title_font_size = 20
                    , title_x=0.0
                #, legend=dict(
                # x=0,
                # y=-0.5)
                    )

    # Margin under Title - Top
    fig.update_layout(margin=dict(t=80))


    # Description Margin - Bottom
    fig.update_layout(margin=dict(b=70))


    # Change Name and Position of Y Axes
    fig.update_yaxes(title=f'{category}'
                #, tickfont=dict(size=16)
                )

    # Change Name and Position of x Axes
    fig.update_xaxes(title= '# releases'
                #,  tickfont=dict(size=16)
                )

    #fig.show()
    st.plotly_chart(fig)

    st.markdown(
    """
        <div style='
            font-size:13px;
            margin-top:-20px;     
            margin-bottom:30px; 
        '>
        🛈 <strong>Note:</strong> A release can be classified under multiple genres/styles, therefore a release may be counted multiple times.
        </div>
        """,
    unsafe_allow_html=True
    )
#vis_distribution('genres')

def vis_share(category, color):
    df_vis_share = df 

    fig = px.pie(df_vis_share.groupby(category).agg(releases = ('release_id' ,'count')).reset_index()
                , names= category
                , values='releases'
                , template='plotly_dark'
                , color_discrete_sequence=color
                #, hover_data='percent'
                #, title='Share of'
                )

    fig.update_traces(textposition='inside'
                    , textinfo='percent+label+value'
                    , insidetextorientation='auto' #radial, tagential, horizontal
                    , texttemplate='<span style="font-family:Segoe UI; font-size:17px;font-weight:750;">%{label}</span><br>' +
                                   '<span style="font-size:12px;">%{percent}</span><br>' +
                                   '<span style="font-size:12px;">%{value}</span>'
         ,
           textfont=dict(
        #size=15,
        color='white'
    ),
        marker=dict(
            line=dict(color='#000000', width=1)  # segregation line
        )
    )                
                                  
    # Chart Title
    fig.update_layout(title=f'{category}' #Share of
                    , title_font_size = 17
                    , title_x=0
                    , legend=dict(
                            x=0.5,
                            y=-0.2,
                            xanchor='center',
                            yanchor='bottom'
                        )
                    )

    #fig.show()
    st.plotly_chart(fig)
#vis_share()




# Title
st.title('Discogs Dashboard')

data = st.secrets['file_path']
#data = 'discogs_data_latest.csv'

# session_state
#if 'df' not in st.session_state:
 
@st.cache_data
def load_data(data):
# Read Data
    df = pd.read_csv(data)
    df = df.iloc[:, 1:]
    df[['country','styles']].fillna(value='-')
    df.fillna(value='')
    df['genres'] = df['genres'].str.replace(r'Folk\s*,\s*World\s*,\s*& Country','Folk & World & Country',regex=True)
    df['release_id'] = df['release_id'].astype(str)
    df['year'] = df['year'].astype(str)
    #df['year'] = pd.to_datetime(df['year']).dt.year
    df['LP vs. EP'] = np.where(df['formats'].str.contains('Album|LP'),'LP','EP')
    df['Reissue/Remaster'] = np.where(df['formats'].str.contains('Reissue|Remaster'),'Reissue/Remaster','-')
    df['Coloring'] = np.where(df['Collection vs. Wantlist'].str.contains('Collection'),'🟢','🔴')
    df['artist'] = df['artist'].str.replace(r'\(\d+\)', '', regex=True).str.strip()
    #df['artist_sort'] = df['artist_sort'].str.replace(r'\(\d+\)', '', regex=True).str.strip()
    df['label'] = df['label'].str.replace(r'\(\d+\)', '', regex=True).str.strip()
    #df= df.sort_values(by="release_id", ascending=True)
    return(df)

# without session_state
df = load_data(data)
#st.session_state.df = load_data(data)


#if 'df' in st.session_state:
    #df = st.session_state.df


# -- Preparation Slicer/Filter --

styles = sorted(set(df['styles'].dropna().str.split(',').explode().str.strip()) - {''})   
genres = sorted(set(df['genres'].dropna().str.split(',').explode().str.strip())) # sorted((set(df['genres'].dropna().str.split(',').explode().str.strip()) - {'Folk', 'World', '& Country'}) | {'Folk, World, & Country'}) 
label = sorted(set(df['label'].dropna().str.split(',').explode().str.strip()) - {''})
year = sorted(set(df['year'].dropna().unique().tolist()), reverse = True)
artist = sorted(set(df['artist'].dropna().str.split(',').explode().str.strip()) - {''})
collection_wantlist = sorted(set(df['Collection vs. Wantlist'].dropna().str.split(',').explode().str.strip()) - {''})
remaster_reissue = sorted(set(df['Reissue/Remaster'].dropna().str.split(',').explode().str.strip()) - {''})
  


# -- Slicer & Filter --

col1, col2 = st.columns(2)

with col1:
    artist_filter = st.multiselect(
        'Artist',
        artist
    )
with col2:
    label_filter = st.multiselect(
        'Label',
        label
    )
with col1:
    genres_filter = st.multiselect(
        "Genres",
        genres
    )
with col2:
    styles_filter = st.multiselect(
        'Styles',
        styles
    )
with col1:
    collection_wantlist_filter = st.multiselect(
        'Collection vs. Wantlist',
        collection_wantlist 
    )
with col2:
    remaster_reissue_filter = st.multiselect(
        'Reissue/Remaster',
        remaster_reissue 
    )
# with col1:
#     year_filter = st.multiselect(
#         'Year',
#         year
#     )
#with col1:
year_filter = st.select_slider("Year", sorted(year),(year[0],year[-1]))




# -- Data Filter --

start_jahr, end_jahr = year_filter

df = df[df['styles'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in styles_filter)) &
        df['genres'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in genres_filter)) &
        #(df['year'].isin(year_filter) if year_filter else True) &
        ((df['year'] >= start_jahr) & (df['year'] <= end_jahr) if year_filter else True) &
        (df['label'].isin(label_filter) if label_filter else True) &
        (df['artist'].isin(artist_filter) if artist_filter else True) &
        (df['Collection vs. Wantlist'].isin(collection_wantlist_filter) if collection_wantlist_filter else True) &
        (df['Reissue/Remaster'].isin(remaster_reissue_filter) if remaster_reissue_filter else True)
            ]
        # Ternary Operator

# df = df[(df['styles'].isin(styles_filter) if styles_filter else df['styles'].notna()) &
#         (df['genres'].isin(genres_filter) if genres_filter else df['genres'].notna()) &
#         # df['styles'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in styles_filter)) &
#         # df['genres'].apply(lambda x: all(re.search(rf'\b{re.escape(term)}\b', str(x)) for term in genres_filter)) &
#         #(df['year'].isin(year_filter) if year_filter else True) &
#         ((df['year'] >= start_jahr) & (df['year'] <= end_jahr) if year_filter else True) &
#         (df['label'].isin(label_filter) if label_filter else True) &
#         (df['artist'].isin(artist_filter) if artist_filter else True) &
#         (df['Collection vs. Wantlist'].isin(collection_wantlist_filter) if collection_wantlist_filter else True) &
#         (df['Reissue/Remaster'].isin(remaster_reissue_filter) if remaster_reissue_filter else True)
#             ]
        # Ternary Operator



# -- Calculations ---

all_kpi = df['release_id'].nunique()
collection_kpi = df[df['Collection vs. Wantlist'] == 'Collection']['release_id'].nunique()
wantlist_kpi = df[df['Collection vs. Wantlist'] == 'Wantlist']['release_id'].nunique()
df['Update_Datetime'] = pd.to_datetime(df['Update_Datetime'])
last_update_kpi = str(df['Update_Datetime'].dt.date.unique()[0])



# --- Key Metrcis ---

first_col, second_col, third_col, fourth_col = st.columns(4)
with first_col:
    st.metric(label = 'Collection' 
             ,value = collection_kpi
            )
with second_col:
    st.metric(label = 'Wantlist' 
             ,value = wantlist_kpi,
            )
with third_col:
    st.metric(label = 'Total'
             ,value = all_kpi 
            )
with fourth_col:
    st.metric(label = 'Last data extraction'
             ,value = last_update_kpi
            )
    


# -- Visualizations --

tab1, tab2 = st.tabs(["Genres", "Styles"])
with tab1:
    vis_distribution('genres')
with tab2:
    vis_distribution('styles')

#with st.expander("Details zu Visual 1"):
tab1, tab2 = st.tabs(["Collection vs. Wantlist", "Reissue/Remaster"])
with tab1:
    vis_time_series('Collection vs. Wantlist', px.colors.qualitative.Bold)
with tab2:
    vis_time_series('Reissue/Remaster', px.colors.qualitative.Vivid)

with st.expander("Shares of ⬇️"):
    col1, col2, col3 = st.columns(3)
    with col1:
        vis_share('LP vs. EP', px.colors.qualitative.Plotly)
    with col2:
        vis_share('Collection vs. Wantlist', px.colors.qualitative.Bold)
    with col3:
        vis_share('Reissue/Remaster', px.colors.qualitative.Vivid)



# -- Display Data ---
# st.subheader('Dynamic Filters')
# dynamic_filters.display_df(width = 1500, height = 800)
st.subheader('Discogs Dataset')
#st.dataframe(df, width = 1200, height = 500)
st.dataframe(df[['release_id','title','artist','label','year','country','genres','styles','tracklist','formats','LP vs. EP','Reissue/Remaster','Collection vs. Wantlist','url']], use_container_width=True)




# -- Release Gallery --

# -- Release Gallery --
st.subheader('Release Gallery')
num_columns = 4  
cover_data = df.dropna(subset=["first_image_uri"]).reset_index()
card_height = "625px"  

cols = st.columns(num_columns)
for i, row in cover_data.iterrows():
    with cols[i % num_columns]:
        with st.container():
            st.markdown(
                f"""
                <div style='
                    height: {card_height};
                    padding: auto;  
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    text-align: left;
                '>
                    <div style='width: 100%; height: 0; padding-bottom: 100%; position: relative;'>
                        <img src='{row['first_image_uri']}' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;'>
                    </div>
                    <div style='flex-grow: 1; padding-top: 12px; font-size: 16px;'>
                        <div style='text-align: center;'>
                            <p><a href='{row['url']}' target='_blank'><strong>{row['title']} ({row['year']})</strong></a></p>
                        </div>
                        <div style='text-align: left;'>
                        <p>🎤 Artist: {row['artist']}</p>
                        <p>🏷️ Label: {row['label']}</p>
                        <p>🎶 Genre: {row['genres']}</p>
                        <p>🖌️ Styles: {row['styles']}</p>
                        <p> {row['Coloring']} {row['Collection vs. Wantlist']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            #st.markdown("---")
        st.markdown("---")
