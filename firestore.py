import firebase_admin
from firebase_admin import firestore, credentials


cred = credentials.Certificate('./momo-89849-firebase-adminsdk-c5eue-9601b76f17.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'momo-89849',
})
db = firestore.client()

docs = db.collection('User_Collection').stream()

user_list = []



for doc in docs:
    user_list.append(doc.id)

# print(user_list)


for user in user_list:
    doc_ref = db.collection('User_Collection').document(user).collection('Routine_Collection').stream()

    for doc in doc_ref:
        # print(doc.to_dict())
        print(doc.doc_ref.id)

