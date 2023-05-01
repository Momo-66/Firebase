import firebase_admin
from firebase_admin import firestore, credentials


cred = credentials.Certificate('./key.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'momo-89849',
})
db = firestore.client()

transaction = db.transaction()
docs = db.collection('User_Collection').stream()

user_list = []
routine_list = []

finished_all_users =[] # 루틴을 모두 완료한 유저의 리스트
not_completed_routine = [] #완료하지 않은 유저 리스트
completed_routine = [] # 완료한 유저 리스트

# 전체 유저 가져오기
for doc in docs:
    user_list.append(doc.id)

# 전체 유저 순회
for user in user_list:
    routine_ref = db.collection('User_Collection').document(user).collection('Routine_Collection').stream()
    is_all_finished = True
    
    user_routine_dict=[]

    # 현재 user의 user_routine 순회
    for routine in routine_ref:
        user_routine_dict = routine.to_dict()
        print(user, doc.id ,user_routine_dict)

        # user_routine_dict의 finished가 false이면 streak = 0
        if user_routine_dict['finished'] == False:
            user_routine_dict['streak'] = 0 #[UPDATE]streak 0으로 만들어주기
            is_all_finished = False
        #routine을 완료한 경우 streak +1
        elif user_routine_dict['finished'] == True:
            user_routine_dict['streak'] += 1 #[UPDATE] streak +1
            user_routine_dict['finished'] += False #[UPDATE]streak 0으로 만들어주기

    if is_all_finished == True:
        finished_all_users.append(user)

# @firestore.transactional
def streak_plus(transaction, use):
    routine_ref = db.collection('User_Collection').document(use)
    snapshot = routine_ref.get(transaction=transaction)
    new_streak = snapshot.get('streak') + 1
    transaction.update(routine_ref, {
        'streak': new_streak
    })

# 전체 유저 가져오기
for doc in docs:
    user_list.append(doc.id)

# 전체 유저 순회
for user in user_list:
    routine_ref = db.collection('User_Collection').document(user).collection('Routine_Collection').stream()
    is_all_finished = True
    
    user_routine_dict=[]

    # 현재 user의 user_routine 순회
    for routine in routine_ref:
        user_routine_dict = routine.to_dict()
        print(user, doc.id ,user_routine_dict)

        # user_routine_dict의 finished가 false이면 streak = 0
        if user_routine_dict['finished'] == True:
            completed_routine.append(routine)
        #routine을 완료한 경우 streak +1
        elif user_routine_dict['finished'] == False:
            not_completed_routine.append(routine)

@firestore.transactional
def streak_zero(transaction, use):
    routine_ref = db.collection('User_Collection').document(user).collection('Routine_Collection').stream()
    # snapshot = routine_ref.get(transaction=transaction)
    new_streak = 0
    completed = 'false'
    transaction.update(routine_ref, {
        'completed' : completed,
        'streak': new_streak
    })
    
def refresh_completed(transaction, use):
    routine_ref = db.collection('User_Collection').document(use).collection('Routine_Collection').stream()
    snapshot = routine_ref.get(transaction=transaction)
    new_streak = snapshot.get('streak') +1
    completed = 'false'
    transaction.update(routine_ref, {
        'completed': completed,
        'streak' : new_streak
    })

for u in finished_all_users:
    streak_plus(transaction, u)

for u in completed_routine:
    refresh_completed(transaction, u)

for u in not_completed_routine:
    streak_zero(transaction, u)