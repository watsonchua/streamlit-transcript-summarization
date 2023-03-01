import streamlit as st
import pandas as pd
import re

transcription_order = ['NLB Manual', 'NLB Auto', 'Transcribe (Current)', 'Transcribe (Upcoming)']

@st.cache_data()
def read_df():
    df = pd.read_csv('./df_summaries.csv')
    df['transcription_method'] = df['transcription_method'].apply(lambda x: 'Transcribe (Current)' if x == 'Transcribe' else 'Transcribe (Upcoming)' if x=='Whisper'  else x)

    return df



def escape_markdown(text):
    # replace $
    if text is None:
        return None
        
    parse = re.sub(r"(\$)", r"\\\1", text)
    return parse

    # parse = re.sub(r"([_*\[\]()~`>\#\+\-=|\.!]$)", r"\\\1", text)
    # reparse = re.sub(r"\\\\([_*\[\]()~`>\#\+\-=|\.!])", r"\1", parse)
    # return reparse 

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
        all_summarizers = ['All'] + [m for m in sorted(df['summary_method'].unique()) if m != 'None']
        summarizer_filter = st.multiselect('Summariser(s)', all_summarizers, default=all_summarizers)
    
        if 'All' in summarizer_filter:
            summarizer_filter = all_summarizers


        # # transcription filter
        all_transcriptions = ['All'] + [m for m in sorted(df['transcription_method'].unique()) if m != 'Synopsis']
        transcription_filter = st.multiselect('Transcription(s)', all_transcriptions, default=all_transcriptions)
    
        if 'All' in transcription_filter:
            transcription_filter = all_transcriptions
    
    df_synopsis = df[(df["file_id"] == file_select) & (df['transcription_method'] == 'Synopsis')]
    synopsis = df_synopsis.iloc[0]['summary'] if len(df_synopsis) > 0 else None
    df_filtered = df[(df["file_id"] == file_select) & (df['transcription_method'].isin(transcription_filter)) & (df['summary_method'].isin(summarizer_filter))]
    # df_filtered = df[(df["file_id"] == file_select) & (df['summary_method'].isin(summarizer_filter))]

    with st.container():
        st.subheader('Transcripts')

        manual_transcript_col, others_transcript_col = st.columns((1,1))
        with manual_transcript_col:
            manual_transcript_text = df[(df["file_id"] == file_select) & (df['transcription_method']=='NLB Manual')]['transcript'].iloc[0] if len(df[(df["file_id"] == file_select) & (df['transcription_method']=='NLB Manual')]) > 0 else None
            with st.expander('NLB Manual', expanded=True):
                st.text_area(label='', value=manual_transcript_text, height=500)


        
        with others_transcript_col:
            for tm in [t for t in transcription_order if t in df_filtered['transcription_method'].unique()]:
            # for tm in transcription_order:
                if tm == 'NLB Manual':
                    continue
                df_tm_filtered = df_filtered[df_filtered['transcription_method']==tm]
                if len(df_tm_filtered) > 0:
                    with st.expander(tm):
                        st.text_area(label='', value=df_tm_filtered.iloc[0]['transcript'], height=500)



        # st.text_area("Synopsis", value=synopsis)


    
    with st.container():
        st.subheader('Summaries')

        manual_col, others_col = st.columns((1,1))

        # with st.expander("Synopsis", expanded=True):
        #     st.write(escape_markdown(synopsis))

        with manual_col:
            st.markdown('**_Manual Sypnosis_**')
            with st.expander('Manual Sypnosis', expanded=True):
                st.write(escape_markdown(synopsis))


        

        with others_col:
            st.markdown('**_Sypnosis from Transcriptions_**')
            # for tm in transcription_order:
            # for tm in sorted(df_filtered['transcription_method'].unique()):
            for tm in [t for t in transcription_order if t in df_filtered['transcription_method'].unique()]:
                    df_tm_filtered = df_filtered[df_filtered['transcription_method']==tm]
                    if len(df_tm_filtered) > 0:
                        with st.expander(tm):
                            for index, row in df_tm_filtered.iterrows():
                                st.caption(row['summary_method'])
                                st.write(escape_markdown(row['summary']))



if __name__ == "__main__":
    main()