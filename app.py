import streamlit as st
import pandas as pd



@st.cache
def read_df():
    df = pd.read_csv('./df_summaries.csv')

    return df


def main():
    st.set_page_config(
        layout="wide",
        page_title="Transcript Summary Viewer"
        )
    st.title("Transcript Summary Viewer")


       


    df = read_df()

    with st.sidebar:
        file_select = st.selectbox(label='File ID', options=sorted(df['file_id'].unique(), reverse=False))


        # summariser filter
        all_summarizers = ['All'] + [m for m in df['summary_method'].unique() if m != 'None']
        summarizer_filter = st.multiselect('Summariser(s)', all_summarizers, default=all_summarizers)
    
        if 'All' in summarizer_filter:
            summarizer_filter = all_summarizers


        # transcription filter
        all_transcriptions = ['All'] + [m for m in df['transcription_method'].unique() if m != 'Synopsis']
        transcription_filter = st.multiselect('Transcription(s)', all_transcriptions, default=all_transcriptions)
    
        if 'All' in transcription_filter:
            transcription_filter = all_transcriptions
    
    df_synopsis = df[(df["file_id"] == file_select) & (df['transcription_method'] == 'Synopsis')]
    # TODO: why are synopsis not showing?
    synopsis = df_synopsis.iloc[0]['summary'] if len(df_synopsis) > 0 else None
    df_filtered = df[(df["file_id"] == file_select) & (df['transcription_method'].isin(transcription_filter)) & (df['summary_method'].isin(summarizer_filter))]
    
    with st.container():
        st.subheader('Transcripts')
        for tm in df_filtered['transcription_method'].unique():
            df_tm_filtered = df_filtered[df['transcription_method']==tm]
            with st.expander(tm):
                st.text_area(label='', value=df_tm_filtered['transcript'].iloc[0], height=500)



        # st.text_area("Synopsis", value=synopsis)


    
    with st.container():
        st.subheader('Summaries')

        with st.expander("Synopsis", expanded=True):
            st.write(fr"{synopsis}")

        for tm in df_filtered['transcription_method'].unique():
            with st.expander(tm):
                df_tm_filtered = df_filtered[df['transcription_method']==tm]
                for index, row in df_tm_filtered.iterrows():
                    # st.text_area(label=row['summary_method'], value=row['content'])
                    st.caption(fr"{row['summary_method']}")
                    st.write(fr"{row['summary']}")



if __name__ == "__main__":
    main()