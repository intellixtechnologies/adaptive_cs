import sqlalchemy
import json
import datetime
import warnings
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.stem.snowball import SnowballStemmer

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])



#API for getphone number from VOX
def getPhoneNumber():
    pass #API to get phone number of incoming call from Vox API

#API for dialogflow fulfillment
def dialogFlowFulfilment():
    pass #API to ensure dialogflow fulfiment. Internally uses webhook operations
    #Handle Dialogflow webhook operations
    def DialogFlowconnect():
        return 1 # Code for dialogflow connector


#Predict Team Name,component and classification based on model
# Provide the location of selected models to be used. 
# Output is Predicted Team Name, Component and Classification
def predict_TeamName_Component_Classification(defect_summary=''):
    #connect models to determine based on text summary
    #Load Models
    predictions ={}
    model_Team_Name = pickle.load(
        open(
             os.getcwd()+"/outputs/Team Name_SVM_RS.model", "rb"
        )
    )
    model_Component = pickle.load(
        open(
             os.getcwd()+"/outputs/Component_SVM_RS.model", "rb"
        )
    )
    model_Classification = pickle.load(
        open(
             os.getcwd()+"/outputs/Classification_SVM_RS.model", "rb"
        )
    )
    
    pred_Team_Name = model_Team_Name.predict(defect_summary)[0]
    pred_Component = model_Component.predict(defect_summary)[0]
    pred_Classification =model_Classification.predict(defect_summary)[0]
    
    predictions = {'Team_Name':pred_Team_Name, 'Component':pred_Component, 'Classification':pred_Classification }
    
    return(predictions)


#Sentiment Analysis of user query based on Vader (Valence Aware Dictionary and sEntiment Reasoner)
def get_sentiment(input_text):
    import nltk
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sentiment = SentimentIntensityAnalyzer()
    print("Sentiment Score ",sentiment.polarity_scores(input_text)['compound'])
    return(sentiment.polarity_scores(input_text)['compound'])



#Custom Logic to determine negative sentiment in order to redirect user to Senior Manager based on values of VADER and DF sentiments.
def detect_user_neg_sentiment(df_sentiment=0, vader_sentiment=0):
    #Send to manager if Dialogflow and custom analysis both suggest really negative sentiment and low CSI
    if (df_sentiment <= -0.8) and (vader_sentiment <=-0.7): 
        return(True)
    else:
        return(False)


#Get Team ID based on Team Name
def get_team_id(team_name=''):
    stmt = sqlalchemy.text("SELECT TEAM_ID FROM pub.team_master where TEAM_NAME ='"+team_name+"';")
    db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})
    team_id=''
    try:
        with db.connect() as conn:
            results = conn.execute(stmt).fetchall()
            for result in results:
                #print(type(result))
                for column, value in result.items():
                    if(column == 'TEAM_ID'):
                        team_id = value
                        #print(team_id)
        return(team_id)
    except Exception as e:
        return 'Error: {}'.format(str(e))

#Get Component ID based on Component Name
def get_component_id(component=''):
    stmt = sqlalchemy.text("SELECT COMPONENT_ID FROM pub.component_master where COMPONENT ='"+component+"';")
    db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})
    component_id=''
    try:
        with db.connect() as conn:
            results = conn.execute(stmt).fetchall()
            for result in results:
                #print(type(result))
                for column, value in result.items():
                    if(column == 'COMPONENT_ID'):
                        component_id = value
                        #print(team_id)
        return(component_id)
    except Exception as e:
        return 'Error: {}'.format(str(e))
    

#Get Classification ID based on Classification
def get_classification_id(classification=''):
    stmt = sqlalchemy.text("SELECT CLASS_ID FROM pub.classification_master where CLASSIFICATION ='"+classification+"';")
    db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})
    class_id=''
    try:
        with db.connect() as conn:
            results = conn.execute(stmt).fetchall()
            for result in results:
                #print(type(result))
                for column, value in result.items():
                    if(column == 'CLASS_ID'):
                        class_id = value
                        #print(team_id)
        return(class_id)
    except Exception as e:
        return 'Error: {}'.format(str(e))



#Custom Triaging Logic to determine whom ticket should be assigned to based on predicted Team Name, Component, Classification and sentiment
def get_Assignee(team_name, component, classification, negative_sentiment=False):
    member_id=''
    assignee=''
    team_id=''
    component_id=''
    class_id=''
    
    #for any negative sentiment assign to Senior Manager
    if (negative_sentiment ==True):
        member_id='A22'
        assignee='Senior Manager'
        db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})
        updstmt = sqlalchemy.text("UPDATE pub.assignee_triage SET ACTIVE_COUNT= ACTIVE_COUNT+1 where MEMBER_ID ='"+member_id+"';")
        print(updstmt)
        try:
        #Increment Active Ticket count for the Assignee
            with db.connect() as conn1:
                results = conn1.execute(updstmt)
                conn1.invalidate()
                conn1.close()
                print("Successful Updation of Active Count")
        except Exception as e:
            return 'Error: {}'.format(str(e))
        return(assignee)    
    
    #if Component is untrigaed then send to Escalation Manager
    if (component =='Untriaged'):
        member_id='A21'
        assignee='Escalation Manager'
        db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})
        updstmt = sqlalchemy.text("UPDATE pub.assignee_triage SET ACTIVE_COUNT= ACTIVE_COUNT+1 where MEMBER_ID ='"+member_id+"';")
        print(updstmt)
        try:
        #Increment Active Ticket count for the Assignee
            with db.connect() as conn1:
                results = conn1.execute(updstmt)
                conn1.invalidate()
                conn1.close()
                print("Successful Updation of Active Count")
        except Exception as e:
            return 'Error: {}'.format(str(e))
        return(assignee)
    else:
        #Triage to Assignee capable of handling such ticket(based on team, component and classification)
        #Assign to the person only if number of active tickets he/she is handling is less than 3
        team_id = get_team_id(team_name)
        component_id = get_component_id(component)
        class_id = get_classification_id(classification)
        stmt = sqlalchemy.text("SELECT MEMBER_ID,NAME FROM pub.assignee_triage where TEAM_ID ='"+str(team_id)+"'"+ 
                               "and COMPONENT_ID ='"+str(component_id)+"'"+" and CLASS_ID like '%"+str(class_id)+"%' and ACTIVE_COUNT<3 LIMIT 1;")
        #print(stmt)
        
        db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})
        component_id=''
        try:
            with db.connect() as conn:
                results = conn.execute(stmt).fetchall()
                if len(results)==0: #For no assignee to triage based on data setup, send to Escalation Manager for manual triage
                    member_id = 'A21'
                    assignee = 'Escalation Manager'
                else:
                    for result in results:
                        #print(type(result))
                        for column, value in result.items():
                            if(column == 'MEMBER_ID'):
                                member_id = value
                                #print(member_id)
                            if(column == 'NAME'):
                                assignee = value
                                #print(assignee)
                #Increment Active Ticket count for the Assignee
                updstmt = sqlalchemy.text("UPDATE pub.assignee_triage SET ACTIVE_COUNT= ACTIVE_COUNT+1 where MEMBER_ID ='"+member_id+"';")
                #print(updstmt)
                try:

                    with db.connect() as conn1:
                        results = conn1.execute(updstmt)
                        conn1.invalidate()
                        conn1.close()
                        print("Successful Updation of Active Count")
                except Exception as e:
                    return 'Error: {}'.format(str(e))
                
                
            return(assignee)
        except Exception as e:
            return 'Error: {}'.format(str(e))



#Obtaining customer details (Name, Phone and Email) based on customer phone number
def getCustomerRecordFromDB(request):
    d  = {} 

    phonenum=request['phone']
    print('Received phone number is ',phonenum)
    stmt = sqlalchemy.text("SELECT * FROM pub.customer_master where PHONE_NUM ="+phonenum+";")
    db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})

    try:

        with db.connect() as conn:
            results = conn.execute(stmt).fetchall()
            for result in results:
                #print(type(result))
                for column, value in result.items():
                    if(column == 'NAME'):
                        value = value
                        
                    if(column == 'PHONE_NUM'):
                        value = str(value)
                        

                    if(column == 'EMAIL'):
                        value = str(value)
                        
                    #print("ColumnName:", column , "Value ", value)
                    d = {**d, **{column:value}}
                

            return json.dumps(d)
    except Exception as e:
        return 'Error: {}'.format(str(e))
    return json.dumps(a)


#Method to determine if an unresolved INC is present for a customer
def getINCRecordFromDB(request):
    d , a = {} , []

    phonenum=request['phone']
    #print('Received phone number is ',phonenum)
    stmt = sqlalchemy.text("SELECT * FROM pub.incident_master where Customer_Phone ="+phonenum+" and status <> 'RESOLVED';")
    db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})

    try:

        with db.connect() as conn:
            results = conn.execute(stmt).fetchall()
            for result in results:
                #print(type(result))
                for column, value in result.items():
                    if(column == 'Bug_ID'):
                        value = value
                        
                    if(column == 'Type'):
                        value = str(value)
                        

                    if(column == 'Summary'):
                        value = str(value)
                    
                    if(column == 'Customer_Phone'):
                        value = str(value)
                    
                    if(column == 'Product'):
                        value = str(value)
                    
                    if(column == 'Component'):
                        value = str(value)
                    
                    if(column == 'Assignee'):
                        value = str(value)
                    
                    if(column == 'Status'):
                        value = str(value)

                    if(column == 'Resolution'):
                        value = str(value)
                    
                    if(column == 'Priority'):
                        value = str(value)
                    
                    if(column == 'Classification'):
                        value = str(value)
                    
                    if(column == 'Team_Name'):
                        value = str(value)
                    
                    if(column == 'Filed_via'):
                        value = str(value)    
                    #print("ColumnName:", column , "Value ", value)
                    d = {**d, **{column:value}}
                a.append(d)

            return json.dumps(a)
    except Exception as e:
        return 'Error: {}'.format(str(e))
    return json.dumps(a)


#Method for creating a new INC record for a customer
def InsertINCRecord(request):
    d = {}
    bug_id=''
    
    stmt=sqlalchemy.text("select MAX(BUG_ID)+1 as BUGID from pub.incident_master;")
    db = sqlalchemy.create_engine('mysql://root:password@localhost:3306/pub',connect_args={'autocommit': True})
    try:
        
        with db.connect() as conn1:
            results = conn1.execute(stmt).fetchall()
            for result in results:
                #print(type(result))
                for column, value in result.items():
                    if(column == 'BUGID'):
                        bug_id = value
            conn1.invalidate()
            conn1.close()
    except Exception as e:
        return('Error: {}'.format(str(e)))

    
    
    Bug_ID=bug_id
    Type='defect'
    Summary=request['Summary']
    Customer_Phone=request['Customer_Phone']
    Product=request['Product']
    Component=request['Component']
    Assignee=request['Assignee']
    Status='ACTIVE'
    Resolution=''
    Priority='P3'
    Classification=request['Classification']
    Team_Name=request['Team_Name']
    Filed_via='Phone'
    print('Creating New INC')
    sqlinsert = sqlalchemy.text("INSERT INTO pub.incident_master VALUES('"+str(Bug_ID)+"','"+Type+"','"+Summary+ "','"+Customer_Phone+ 
                           "','"+Product+"','"+Component+"','"+Assignee+"','"+Status+"','"+Resolution+"','"+Priority+"','"+Classification+
                           "','"+Team_Name+"','"+Filed_via+"' );")
    
    #print(sqlinsert)
    try:

        with db.connect() as conn:
            results = conn.execute(sqlinsert)
            conn.invalidate()
            conn.close()
            return json.dumps("Successful Insertion")
    except Exception as e:
        return 'Error: {}'.format(str(e))
    finally:
        db.dispose()



#Flow for a scenario where unresolved incident exists for a customer
def incident_status_flow(phone,customer_name,customer_email,inc_no,inc_summary,assignee):
    print('Hi '+customer_name+'. Thank you for calling us. As I can see, you have an open ticket with us.')
    print('Let me get you the details for the same. The ticket '+str(inc_no) +' for the issue '+inc_summary+ ' is currently being worked upon by '+ 
          assignee+'.'+' Do you want me to connect you with the executive?')
    return 1 #Output to be passed to DialogFlow connector to be passed on to the customer

#Flow for a scenario where new incident is being created for the customer
def new_incident_flow(phone, customer_name,customer_email,inc_summary):
    Team_Name,Component,Classification, Assignee = '','','',''
    df_sentiment, vader_sentiment = 0,0
    neg_sentiment = False
    req={}
    issue_summary = inc_summary#'Javascript error while opening webpages' #obtained from dialogflow connector 
    Team_Name = predict_TeamName_Component_Classification([issue_summary])['Team_Name']
    Component = predict_TeamName_Component_Classification([issue_summary])['Component']
    Classification = predict_TeamName_Component_Classification([issue_summary])['Classification']
    df_sentiment = -0.3 #obtained from dialogflow connector based on issue_summary
    vader_sentiment = get_sentiment(issue_summary)
    neg_sentiment = detect_user_neg_sentiment(df_sentiment, vader_sentiment)
    
    Assignee = get_Assignee(Team_Name, Component, Classification, neg_sentiment)
    
    req['Summary'] = issue_summary
    req['Customer_Phone'] = phone
    req['Product'] = 'Firefox'
    req['Component'] = Component 
    req['Assignee'] = Assignee
    req['Classification'] = Classification
    req['Team_Name'] = Team_Name
    
    InsertINCRecord(req)
    print('Hi '+customer_name+'. Thank you for your patience. An incident has been raised and assigned to '+Assignee+
         ' Let me connect you with the executive ')   #pass success message to DialogFlow Connector to be passed on to the customer.



#Master method for determining the process flows for Adaptive CS
def adaptive_cs(req):
    phone,customer_name,customer_email,inc_no,inc_summary,assignee = '','','','','',''
    phone = req['phone']
    #print(getCustomerRecordFromDB(req))
    customer_name = json.loads(getCustomerRecordFromDB(req))['NAME']
    customer_email = json.loads(getCustomerRecordFromDB(req))['EMAIL']
    #print(getINCRecordFromDB(req))
    if getINCRecordFromDB(req)!= '[]':
        inc_no = json.loads(getINCRecordFromDB(req))[0]['Bug_ID']
        inc_summary = json.loads(getINCRecordFromDB(req))[0]['Summary']
        assignee = json.loads(getINCRecordFromDB(req))[0]['Assignee']
    
    if (inc_no != ''):
        incident_status_flow(phone,customer_name,customer_email,inc_no,inc_summary,assignee)
    else:
        print('Hi '+ customer_name +'. Thank you for calling us. Please tell us about the issue that you are facing')
        inc_summary = input("Summary of the issue: ")
        new_incident_flow(phone, customer_name,customer_email,inc_summary)

if __name__ == "__main__":
    req = {"phone": "14699555304"} #Details of phone number to be obtained from VoxImplant API (getPhoneNumber)
    adaptive_cs(req) #pass request and adaptive_cs will determine rest of the flow based on underlying logic, predictions, sentiment analysis etc.
