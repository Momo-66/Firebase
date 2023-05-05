import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'momo-89849',
})
db = firestore.client()
transaction = db.transaction()
docs = db.collection('User_Collection').stream()

user_list = [] #전체 유저 리스트
routine_list = [] #전체 루틴 리스트

finished_all_users = [] #전체 루틴 완료한 유저
finished_not_users = [] #전체 루틴 완료하지 않은 유저
completed_routine = [] #완료된 루틴
not_completed_routine = [] #완료되지 않은 루틴

# # 전체 유저 가져오기
for doc in docs:
    user_list.append(doc.id)

# 전체 루틴 리스트 가져오기
for user in user_list:
    routine_ref = db.collection('User_Collection').document(user).collection('Routine_Collection').stream()
    for routine in routine_ref:
        user_routine_dict = routine.to_dict()
        routine_list.append(routine) 
        
        
for user in user_list:
    routine_ref = db.collection('User_Collection').document(user).collection('Routine_Collection').stream()
    is_all_finished = True
    
    user_routine_dict=[]

    # 현재 user의 user_routine 순회
    for routine in routine_ref:
        user_routine_dict = routine.to_dict()
        # 루틴을 완료하지 않은 경우
        if user_routine_dict['finished'] == False:
            finished_not_users.append(user) #user streak 초기화
            not_completed_routine.append(routine) #user streak 초기화 & finished:False로 초기화
            is_all_finished = False
        # 루틴을 완료한 경우
        elif user_routine_dict['finished'] == True:
            completed_routine.append(routine) #routine streak +1 & finished:False 초기화
    #사용자가 전체 루틴을 완료한 경우
    if is_all_finished == True:
        finished_all_users.append(user)

@firestore.transactional

# #유저 streak 추가(완)
def streak_plus(transaction, user):
    routine_ref = db.collection('User_Collection').document(user)
    snapshot = routine_ref.get(transaction=transaction)
    new_streak = snapshot.get('streak') + 1
    transaction.update(routine_ref, {
        'streak': new_streak
    })

for u in finished_all_users:
    streak_plus(transaction, u)