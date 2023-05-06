
from Model import Model

test_set = {
    'user1': {
        'remedy_type': 'pack',
        'conditions': ['oily', 'cleansing','dark spots'],
        'actual_indices': [301,308,309,311,325,476,336]
    },
    'user2': {
        'remedy_type': 'cream and moisturizer',
        'conditions': ['acne', 'pigmentation','dark spots'],
        'actual_indices': [1004, 1005, 1114,999,1000]
    },
    'user3': {
        'remedy_type': 'mask',
        'conditions': ['dark circle', 'wrinkles','anti ageing'],
        'actual_indices': [670, 688, 690, 747,750]
    },
    'user4': {
        'remedy_type': 'scrub',
        'conditions': ['dry', 'anti ageing','open pores'],
        'actual_indices': [101, 138, 150]
    },
    'user5': {
        'remedy_type': 'oil and toner and serum',
        'conditions': ['glowing', 'moisturising','brightening'],
        'actual_indices': [1201, 1281, 1296,1320,1355,1401,1406,1435]
    },
    'user6': {
        'remedy_type': 'treatment',
        'conditions': ['whitening', 'tan'],
        'actual_indices': [1519, 1531]
    },
     'user7': {
        'remedy_type': 'scrub',
        'conditions': ['dry', 'dark circle','open pores'],
        'actual_indices': [8]
    },
     'user8': {
        'remedy_type': 'cream and moisturizer',
        'conditions': ['whitening', 'glowing'],
        'actual_indices': [903,905,914,919,928,929,939,948,988,1033,1034,1035,1036,1045]
    },
    'user9': {
        'remedy_type': 'cream and moisturizer',
        'conditions': ['whitening', 'glowing'],
        'actual_indices': [903,905,914,919,928,929,939,948,988,1033,1034,1035,1036,1045,]
    },
    'user10': {
        'remedy_type': 'oil and toner and serum',
        'conditions': ['whitening', 'wrinkles','anti ageing'],
        'actual_indices': [1225]
    },
   'user11': {
        'remedy_type': 'treatment',
        'conditions': ['whitening', 'wrinkles','anti ageing'],
        'actual_indices': [1519]
    },
    'user12': {
        'remedy_type': 'treatment',
        'conditions': ['wrinkles','open pores','oily'],
        'actual_indices': []
    },'user13': {
        'remedy_type': 'treatment',
        'conditions': ['open pores','oily'],
        'actual_indices': [1510]
    },
    'user14': {
        'remedy_type': 'treatment',
        'conditions': ['whitening','brightening'],
        'actual_indices': [1739,1746,1754]
    },
    'user15': {
        'remedy_type': 'treatment',
        'conditions': ['dark spot','pimple','pigmentation'],
        'actual_indices': [1649]
    },
    'user16': {
        'remedy_type': 'mask',
        'conditions': ['dark spot','pimple','pigmentation'],
        'actual_indices': [695,741,848]
    },
    'user17': {
        'remedy_type': 'mask',
        'conditions': ['whitening','pigmentation'],
        'actual_indices': [643,644,646,680,727,773,848]
    },
    'user18': {
        'remedy_type': 'mask',
        'conditions': ['pimple','acne','oily'],
        'actual_indices': [717,834,861,790]
    },
    'user19': {
        'remedy_type': 'pack',
        'conditions': ['pimple','dark spot','pigmentation'],
        'actual_indices': [476,528]
    },
    'user20': {
        'remedy_type': 'cream and moisturizer',
        'conditions': ['dark spot','pigmentation'],
        'actual_indices': [919,922,926,930,934,936,946,961,965,972]
    },
    'user21': {
        'remedy_type': 'cream and moisturizer',
        'conditions': ['tan','whitening','glowing'],
        'actual_indices': [1048]
    },
    'user22': {
        'remedy_type': 'cream and moisturizer',
        'conditions': ['open pores','anti ageing'],
        'actual_indices': [958,1000,1056,1058,1064,1142]
    },
    'user23': {
        'remedy_type': 'scrub',
        'conditions': ['glowing','brightening','whitening'],
        'actual_indices': [239,2,5,239]
    },
    'user24': {
        'remedy_type': 'oil and toner and serum',
        'conditions': ['moisturising','dullness','dry'],
        'actual_indices': [1201,1294,1324,1328]
    },
    'user25': {
        'remedy_type': 'oil and toner and serum',
        'conditions': ['cleansing'],
        'actual_indices': [1213,1235,1237,1302,1304]
    }

}

# Load the model
model = Model('E:\FYP\DATASET\Remedy Dataset -( the final remedy recomendation dataset ) - final sheet .csv')

# the way to check how many preditions are correct 
correct_user_count = 0
incorrect_user_count = 0

for user, data in test_set.items():
    # Get the actual indices
    actual_indices = set(data['actual_indices'])

    # Get the predicted indices
    predicted_indices = set(model.recommend_remedies(data['remedy_type'], data['conditions'])[0])
    
    # Check if the actual values in each remedy were included in the predicted indices
    correct = all([idx in predicted_indices for idx in actual_indices])
    if correct:
        correct_user_count += 1
        print(correct_user_count)
    else:
        incorrect_user_count += 1

pecentage_of_correct_predictions= correct_user_count / 25


print(f"Finding the accuracy by 25 users: {pecentage_of_correct_predictions:.2f}")
print(f"Number of incorrect predictions for the 25 interates : {incorrect_user_count}")


# testing method second 

# Iterate through the test set
total_predictions = 0
correct_predictions = 0
for user, data in test_set.items():
    # Get the actual indices
    actual_indices = set(data['actual_indices'])

    # Get the predicted indices
    predicted_indices = set(model.recommend_remedies(data['remedy_type'], data['conditions'])[0])

    # Count the correct predictions
    total_predictions += len(predicted_indices)
    correct_predictions += len(actual_indices.intersection(predicted_indices))
print(correct_predictions)

# Calculate the accuracy
accuracy = correct_predictions / total_predictions

print(f"Accuracy: {accuracy:.2f}")
