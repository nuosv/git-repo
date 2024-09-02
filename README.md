# AI Engineer Application Test

**This document as well as the accompanying data is confidential and thus should not be shared with anyone other than the applicant during or after the test**

SWORD Health offers patients the possibility of having physical therapy sessions in the comfort of their homes by prescribing them a set of exercises and providing them with a system that measures their movement and determines whether each of those exercises was correctly performed or not.

On some occasions, during the usage of the system, the patient may have trouble performing an exercise due to technical issues. 
Because this must be avoided at all costs, monitoring exercise quality in the field is crucial for SWORD Health’s success. 
To that end, we collect data regarding every exercise performed by every patient in a given moment in time. 
Each record of the collected data is stored in a table named `exercise_results` containing the following fields:

| Field                      | Meaning |
| :---                       | :---    |
| `session_exercise_result_id` | Identifier of an exercise performed by a patient in a given moment in time (primary key). Each time a patient performs the same exercise, even if in the same session, it will have a different `session_exercise_result_id`. |
| `session_group`              | Identifier of the physical therapy session in which this exercise was performed. Each time a patient performs a session it will have a different `session_group`(all exercises of the same session will have the same value).
| `exercise_name`              | Name of the performed exercise. |
| `exercise_side`              | Body side that the exercise regards. |
| `exercise_order`             | Order of the exercise within the session (the first exercise of the session has `order` 1, the second has `order` 2 and so on). |
| `prescribed_repeats`         | Number of repetitions (individual movements) the patient was supposed to perform in this specific exercise. Can be different among two performances of the same exercise in the same session. The exercise finishes when the number of performed repetitions - either correct or wrong - reaches this value. |
| `training_time`              | Time, in seconds, the patient spent performing the exercise |
| `CM`                         | Number of correct repetitions performed. |
| `WM`                         | Number of incorrect repetitions due to the patient performing the movement incorrectly. |
| `ITE`                        | Number of incorrect repetitions performed due to the patient taking too long to assume the position in which the exercise starts. |
| `WTE`                        | Number of incorrect repetitions performed due to the patient taking too long to finish the repetition once the start position has been assumed. |
| `GU`                         | Number of incorrect repetitions performed due to the patient giving up midway during the movement. |
| `OML`                        | Number of incorrect repetitions performed due to the patient performing a movement with larger amplitude than they should. |
| `WD`                         | Number of incorrect repetitions performed due to the patient performing a movement in the wrong direction. |
| `leave_exercise`             | If the patient leaves the exercise before finishing it, this field stores the reason why. If the patient leaves the exercise, he is led into the following exercise in the session. |
| `leave_session`              | If the patient leaves the session before finishing it, this field stores the reason why (all exercises of the same session will have the same value). If the patient leaves the session, no more exercises are performed. |
| `app_version`                | Software version of SWORD Health's system with which the session of this exercise was performed (all exercises of the same session will have the same value). A smaller value represents an older version. |
| `pain`                       | Amount of pain between reported by the patient at the end of the session where this exercise was performed, between 0 and 10, where 0 is no pain and 10 is the worst possible pain (all exercises of the same session will have the same value). |
| `fatigue`                    | Amount of fatigue between reported by the patient at the end of the session where this exercise was performed, between 0 and 10, where 0 is no fatigue and 10 is the worst possible fatigue (all exercises of the same session will have the same value). |
| `therapy_name`               | Name of the therapy the patient is undertaking (the same for all exercises in the same session). |
| `condition`                  | Clinical condition of the patient (the same for all exercises in the same session). |
| `quality`                    | Whether the session had technical problems, as reported by the patient at the end of the session (all exercises of the same session will have the same value). |

**1.** In a coding language of your preference, write a script to transform the above data such that each row is indexed by `session_group` (thereby representing a performed session instead of a performed exercise) and has the following fields: 

| Field                           | Meaning |
| :---                            | :---    |
| `session_group`                 | explained above (primary key) |
| `app_version`                   | explained above |
| `pain`                          | explained above |
| `fatigue`                       | explained above |
| `therapy_name`                  | explained above |
| `condition`                     | explained above |
| `leave_session`                 | explained above |
| `quality`                       | explained above |
| `leave_exercise_pain`           | Number of exercises in the session that were left due to reason "pain". |
| `leave_exercise_fatigue`        | Number of exercises in the session that were left due to reason "fatigue". |
| `leave_exercise_other`          | Number of exercises in the session that were left due to reason "other". |
| `leave_exercise_tired`          | Number of exercises in the session that were left due to reason "tired". |
| `leave_exercise_system_problem` | Number of exercises in the session that were left due to reason "system_problem". |
| `prescribed_repeats`            | Total number of repetitions (among all exercises) the patient was supposed to perform. |
| `training_time`                 | Time, in seconds, the patient spent performing the session. |
| `perc_CM`                       | Percentage of correct repetitions in the session. |
| `perc_WM`                       | Percentage of incorrect repetitions in the session due to the patient performing the movement incorrectly. |
| `perc_ITE`                        | Percentage of incorrect repetitions in the session due to the patient taking too long to assume the position in which the exercise starts. |
| `perc_WTE`                        | Percentage of incorrect repetitions in the session due to the patient taking too long to finish the repetition once the start position has been assumed. |
| `perc_GU`                         | Percentage of incorrect repetitions in the session due to the patient giving up midway during the movement. |
| `perc_OML`                        | Percentage of incorrect repetitions in the session due to the patient performing a movement with larger amplitude than they should. |
| `perc_WD`                         | Percentage of incorrect repetitions in the session due to the patient performing a movement in the wrong direction. |
| `number_exercises`                | Number of exercises performed in the session. |  
| `number_of_distinct_exercises`    | Number of distinct exercises performed in the session. |

To test your code, you can use `exercise_results_labelled.csv` and 
`session_results_labelled.csv` as the input and output, respectively.

**Bonus points:** include also the following fields:

| Field                           | Meaning |
| :---                            | :---    |
| `exercise_with_most_incorrect`  | Name of the exercise with the highest number of incorrect movements, if any. If there are two with the highest number of incorrect movement, you can pick any of them. |
| `first_exercise_skipped`        | Name of the first skipped exercise, if any. |

**2.** In order to avoid asking patients whether the session had technical problems, we want to predict the `quality` field using the remaining information available in `session_results_labelled.csv`. 
Create a Python notebook for that purpose whilst noting the following:
* The source dataset may be either `session_results_labelled.csv` or a transformation of `exercise_results_labelled.csv` with potential changes to add new features
  * In any case, the source dataset must always be indexed by `session_group`
* You should take on this task just as if you were in a real scenario, thereby, among other things, you should:
  * Clearly define the problem to be solved and propose the success metrics you deem appropriate 
  * Explain how you would perform scoping as well as what potential questions you would like to see addressed 
  * Define the sources of data that might be relevant
  * Perform any cleaning, exploration & visualization you deem appropriate
  * Evaluate the performance of your model
  * Present the main conclusions of your work as well as any potential next steps you would follow provided you had more time to work on this project
* You should make your reasoning, considerations and conclusions clear by the means of comments or text
* You are free to use any existing libraries, both ML-related or not
* The approach should be focused on correctness and effectiveness rather than on showcasing ML techniques