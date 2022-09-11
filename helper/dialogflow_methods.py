def detect_intent_texts(texts,sessionid,userName,userPhone):

    project_id = #'numeric-amphora-357514' #DialogFlow project ID to be provided
    session_id = sessionid
    texts = texts
    language_code = 'en-US'

    import dialogflow_v2beta1 as dialogflow
    import helper.py
    session_client = dialogflow.SessionsClient()
    #print("<======Step 1 Passed========>")
    session = session_client.session_path(project_id, session_id)
    #print('Session path: {}\n'.format(session))
    #print('Session Id: '+ str(session_id))
    #for text in texts:
    #print("<======Step 2 Start========>")
    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)
    #print("<======Chat Input========>")   
    #print(text_input)
        # text=texts
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    #print("<======Step response received Passed========>")
    #print('=' * 20)
    #print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (Sentiment: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.sentimentAnalysisResult.queryTextSentiment.score))
    df_sentiment_score = response.query_result.sentimentAnalysisResult.queryTextSentiment.score
    #print('Fulfillment text: {}\n'.format(
    #    response.query_result.fulfillment_text))
    #print(response)
    #return response.json()

    if (response.query_result.action =="input.welcome"):
        req = {"phone": userPhone }
        output = adaptive_cs(req)
        return output
    elif (response.query_result.action != "input.unknown"):
        return 'Sorry I am unable to understand your request. Let me connect you to an operator'
# [END dialogflow_detect_intent_text]