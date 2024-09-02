import pandas as pd
import numpy as np
def data_preprocessing(path):
    data = pd.read_csv(path)
    # Taking care of NaN values:
    data['leave_exercise'] = data['leave_exercise'].fillna('')
    data['leave_session'] = data['leave_session'].fillna('')
    data['leave_exercise_pain'] = data['leave_exercise'].str.contains('pain').astype(int)
    data['leave_exercise_fatigue'] = data['leave_exercise'].str.contains('fatigue').astype(int)
    data['leave_exercise_tired'] = data['leave_exercise'].str.contains('tired').astype(int)
    data['leave_exercise_system_problem'] = data['leave_exercise'].str.contains('system_problem').astype(int)
    data['leave_exercise_other'] = data['leave_exercise'].str.contains('other').astype(int)
    data['number_exercises'] = 1 if data['exercise_name'].any() else 0
    # Adding aux columns:
    data['total_repetitions_performed'] = data['CM'] + data['WTE'] + data['ITE'] + data['GU'] + data['OML'] + data['WD'] + data['WM']
    # Calculate Total Incorrect Moves per Exercise
    data['total_incorrect_moves_in_exercise'] = data['total_repetitions_performed'] - data['CM']
    # Sum incorrect moves and find the max incorrect per session_group
    data['total_incorrect_moves_in_exercise'] = data.groupby(['session_group', 'exercise_name'], as_index=False)[['total_incorrect_moves_in_exercise']].transform('sum')
    data['skipped_exercise'] = (data[data['leave_exercise']!=''])[['exercise_order']]
    # Grouping by session_group:
    data_session_group = data.groupby('session_group', as_index = False).agg(
    app_version=('app_version', 'first'),
    therapy_name=('therapy_name', 'first'),
    condition=('condition', 'first'),
    pain=('pain', 'first'),
    fatigue=('fatigue', 'first'),
    leave_session=('leave_session', 'first'),
    quality=('quality', 'first'),
    leave_exercise_pain=('leave_exercise_pain', lambda x: sum(x == 1)),
    leave_exercise_fatigue=('leave_exercise_fatigue', lambda x: sum(x == 1)),
    leave_exercise_other=('leave_exercise_other', lambda x: sum(x == 1)),
    leave_exercise_tired=('leave_exercise_tired', lambda x: sum(x == 1)),
    leave_exercise_system_problem=('leave_exercise_system_problem', lambda x: sum(x == 1)),
    prescribed_repeats=('prescribed_repeats', 'sum'),
    training_time=('training_time', 'sum'),
    CM=('CM', 'sum'),
    WTE=('WTE', 'sum'),
    ITE=('ITE', 'sum'),
    GU=('GU', 'sum'),
    OML=('OML', 'sum'),
    WD=('WD', 'sum'),
    WM=('WM', 'sum'),
    number_exercises=('number_exercises', 'sum'),
    number_of_distinct_exercises=('exercise_name', 'nunique'),
    total_repetitions_performed=('total_repetitions_performed', 'sum'),
    exercise_with_most_incorrect=('total_incorrect_moves_in_exercise', lambda x: data.loc[x.idxmax(axis=0), 'exercise_name'] if (x.max() > 0) else np.nan),
    first_exercise_skipped=('skipped_exercise', lambda x: data.loc[x.idxmin(), 'exercise_name'] if (x.any()) else np.nan),   
)
    # Calculate the 'perc' for each session group
    data_session_group['perc_CM'] = data_session_group['CM'] / (data_session_group['total_repetitions_performed'])
    data_session_group['perc_CM'] = data_session_group['perc_CM'].replace([np.inf, -np.inf], 0)
    data_session_group['perc_WTE'] = data_session_group['WTE'] / (data_session_group['total_repetitions_performed'])
    data_session_group['perc_WTE'] = data_session_group['perc_WTE'].replace([np.inf, -np.inf], 0)
    data_session_group['perc_ITE'] = data_session_group['ITE'] / (data_session_group['total_repetitions_performed'])
    data_session_group['perc_ITE'] = data_session_group['perc_ITE'].replace([np.inf, -np.inf], 0)
    data_session_group['perc_GU'] = data_session_group['GU'] / (data_session_group['total_repetitions_performed'])
    data_session_group['perc_GU'] = data_session_group['perc_GU'].replace([np.inf, -np.inf], 0)
    data_session_group['perc_OML'] = data_session_group['OML'] / (data_session_group['total_repetitions_performed'])
    data_session_group['perc_OML'] = data_session_group['perc_OML'].replace([np.inf, -np.inf], 0)
    data_session_group['perc_WD'] = data_session_group['WD'] / (data_session_group['total_repetitions_performed'])
    data_session_group['perc_WD'] = data_session_group['perc_WD'].replace([np.inf, -np.inf], 0)
    data_session_group['perc_WM'] = data_session_group['WM'] / (data_session_group['total_repetitions_performed'])
    data_session_group['perc_WM'] = data_session_group['perc_WM'].replace([np.inf, -np.inf], 0)
    # Deleting aux columns from the dataframe
    data_session_group.drop('CM', axis=1, inplace=True)
    data_session_group.drop('WTE', axis=1, inplace=True)
    data_session_group.drop('ITE', axis=1, inplace=True)
    data_session_group.drop('GU', axis=1, inplace=True)
    data_session_group.drop('OML', axis=1, inplace=True)
    data_session_group.drop('WD', axis=1, inplace=True)
    data_session_group.drop('WM', axis=1, inplace=True)
    data_session_group.drop('total_repetitions_performed', axis=1, inplace=True)
    # Save it to a file named 'result.csv'
    return data_session_group.to_csv('./Data/result.csv', index=False)
if __name__ == '__main__':
    data_preprocessing('./Data/exercise_results_labelled.csv')