# Observations and Deductions.

## Setup 1:

- **Training Data**: Training with 66 incorrectly<sup>1</sup> affine-aligned image files (DataSetGoodQual, DataSetMediumQual, DataSetRandomQual).
- **Scaled_Down**: Scaled down to 256x512x64 dimensions.
- **Loss Metric**: Mean Square Error.
- **Batch Size**: 1.
- **Epoch**: 223
- **Early Stopping with patience level 3**: Since batch size was 1, the fluctuation in loss was too noisy and early stopping could not work.
- **Time to Predict**: on GPU: ~6-7 seconds.
- **Result**: imshowpair(), model_weight, and mmi values are saved in *Y:\masterarbeit_results\Setup_1*

## Setup 2:
- **Training Data**: Training with 66 correctly affine-aligned image files (DataSetGoodQual, DataSetMediumQual, DataSetRandomQual).
- **Scaled_Down**: Scaled down to 256x512x64 dimensions.
- **Loss Metric**: Mean Square Error.
- **Batch Size**: 1.
- **Epoch**: 300
- **Early Stopping with patience level 3**: Since batch size was 1, the fluctuation in loss was too noisy and early stopping could not work.
- **Time to Predict**: on GPU: ~6-7 seconds.
- **Result**: imshowpair() and mmi values are saved in *Y:\masterarbeit_results\Setup_2*
  - Additionally, nonlinear-registration<sup>2</sup> results are also saved in the directory *lrv_registered* and *vxm_registered*, respectively.

## Setup 3:
- **Training Data**: Training with 66 correctly affine-aligned image files (DataSetGoodQual, DataSetMediumQual, DataSetRandomQual).
- **Scaled_Down**: Scaled down to 256x512x64 dimensions.
- **Loss Metric**: Normalized Cross Correlation.
- **Batch Size**: 1.
- **Epoch**: 238 (loss_ncc = -0.889). The range of loss_ncc should be [0, -1]
- **Early Stopping**: Disabled.
- **Time to Predict**: on GPU: ~6-7 seconds.
- **Result**: The result of the prediction was very poor and easily visible to the naked eye. Therefore, no error measurement was performed. The nonlinear-registered results<sup>3</sup> are saved in *Y:\masterarbeit_results\Setup_3\vxm_registered*

## Change_000
- **Setup 1** is deleted.
- **Setup 2 and Setup 3** are moved to this folder as **model_mse** and **model_ncc**.
- All the information mentioned above is relevant, except for the fact that only the model weights are saved and not the images<sup>4</sup>.
- **int_steps** : 7

## Change_001  
|      Infos                |                          Content                                                       |
|           :---            |                                :-                                                      |
| main-commit_id            |                                                                                        |
| dev-commit_id             | `3eb5db8eede58b7f3f9136e084619756ccbb6c82`                                             |
| Logs                      | Yes                                                                                    |
| Model_weights             | Yes                                                                                    |
| Showpair                  | No                                                                                     |
| Enc_and_Dec               | Refer config file                                                                      |
| Loss_metric               | Mean Square Error                                                                      |
| GA                        | Yes (33 images)                                                                        |
| Normalized_GA		        | No                                                                                     |
| Training_size		        | 561 (Default + Janelia)                                                                |
| Validation_size	        | 99                                                                                     |
| Use_Validation_data	    | No                                                                                     |
| Time_to_Predict	        |                                                                                        |
| Diffeomorphic		        | No (int_steps = 0)                                                                     |
| Note			            | Early stopping did not work. It is suspected that `mode=min` is the reason for failure.|

## Change_002
|      Infos                |                          Content                                                       |
|           :---            |                                :-                                                      |
| main-commit_id	|                                                                             |
| dev-commit_id 	|  `bc14f7e1e9710f075ad516868904ab427de4755f`                                 |
| Logs			|  Yes                                                                            |
| Model_weights		|  Yes                                                                        |
| Showpair		|  No                                                                             |
| Enc_and_Dec		|  Refer config file                                                          |
| Loss_metric		|  Mean Square Error                                                          |
| GA			|  Yes (33 images)                                                                |
| Normalized_GA		|  Yes                                                                        |
| Training_size		|  561 (Default + Janelia)                                                    |
| Validation_size	|  99                                                                         |
| Use_Validation_data	|  No                                                                     |
| Time_to_Predict	|                                                                             |
| Diffeomorphic		|  No (int_steps = 0)                                                         |
| Note			|  Early stopping worked. `mode=auto` is used.                                    |

## Change_003
|      Infos                |                          Content                                                       |
|           :---            |                                :-                                                      |
| main-commit_id	|                                                                        |        
| dev-commit_id 	|  `4055334265e9a8541355f266fcc18d9a1c5589cc`                            |
| Logs			|  Yes                                                                       |
| Model_weights		|  Yes                                                                   |
| Showpair		|  No                                                                        |
| Enc_and_Dec		|  Refer config file                                                     |
| Loss_metric		|  Mean Square Error                                                     |
| GA			|  Yes (33 images)                                                           |
| Normalized_GA		|  No                                                                    |
| Training_size		|  561 (Default + Janelia)                                               |
| Validation_size	|  99                                                                    |
| Use_Validation_data	|  No                                                                |
| Time_to_Predict	|                                                                        |
| Diffeomorphic		|  No (int_steps = 0)                                                    |
| Note			| Normalized GA is disabled again as there was no much imrovement.                                       |

## Change_004
|      Infos                |                          Content                                                       |
|           :---            |                                :-                                                      |
| main-commit_id	|                                                                        |           
| dev-commit_id 	|  `4055334265e9a8541355f266fcc18d9a1c5589cc`                            |
| Logs			|  Yes                                                                       |
| Model_weights		|  Yes                                                                   |
| Showpair		|  No                                                                        |
| Enc_and_Dec		|  Default                                                               |
| Loss_metric		|  Mean Square Error                                                     |
| GA			|  Yes (33 images)                                                           |
| Normalized_GA		|  No                                                                    |
| Training_size		|  561 (Default + Janelia)                                               |
| Validation_size	|  99                                                                    |
| Use_Validation_data	|  No                                                                |
| Time_to_Predict	|                                                                        |
| Diffeomorphic		|  No (int_steps = 0)                                                    |
| Note			|    Performance is better than previous configuration.                         |

## Change_005
|      Infos                |                          Content                                                       |
|           :---            |                                :-                                                      |
| main-commit_id	|                                                                                                  | 
| dev-commit_id 	|  `f62bb8ab3b4d968b7e03a4a346a51fe288ff2cfd`                                                      |
| Logs			|  Yes                                                                                                 |
| Model_weights		|  Yes                                                                                             |
| Showpair		|  Yes                                                                                                 |
| Enc_and_Dec		|  Default                                                                                         |
| Loss_metric		|  Mean Square Error                                                                               |
| GA			|  Yes (20 images)                                                                                     |
| Normalized_GA		|  No                                                                                              |
| Training_size		|  560 (Default + Janelia)                                                                         |
| Validation_size	|  100                                                                                             |
| Use_Validation_data	|  No                                                                                          |
| Time_to_Predict	|  ~1.9174213409423828s (pc161)                                                                    |
| Diffeomorphic		|  No (int_steps = 0)                                                                              |
| Note			|  NVIDIA RTX A5000 GPU (pc161). GPU_Speicher:  11,2/88,0 GB. Dedizierter GPU_Speicher:  10,6/24,0 GB  |

## Change_006 a.k.a Diffeomorphic registration
|      Infos                |                          Content                                                       |
|           :---            |                                :-                                                      |
| main-commit_id	|  `6e6ab0300e10f2256d153cff91282b28100e5e00`                                                       |    
| dev-commit_id 	|  `20c02f7eafdab364183c6c1f01331a0396613d4c`                                                       |
| Logs			|  Yes                                                                                                  |
| Model_weights		|  Yes                                                                                              |
| Showpair		|  Yes                                                                                                  |
| Enc_and_Dec		|  Default                                                                                          |
| Loss_metric		|  Mean Square Error                                                                                |
| GA			|  Yes (20 images)                                                                                      |
| Normalized_GA		|  No                                                                                               |
| Training_size		|  560 (Default + Janelia)                                                                          |
| Validation_size	|  100                                                                                              |
| Use_Validation_data	|  No                                                                                           |
| Time_to_Predict	|  ~6.9174213409423828s (pc161)                                                                     |
| Diffeomorphic		|  Yes (int_steps = 7)                                                                              |
| Note			|  Diffeomorphic registration. Visual appearance is good, but MMI score is low.   |

# Change_005 vs Change_000
> - Gradient Accumulation
> - Learning rate is decreased from 1e-4 to 1e-3
> - Training images from Janelia dataset.
> - intsteps was 7, now is 0.
> - **Result**: Result seems to have worsened.
>   - **Reason**: int_steps = 7 gives you good result.
> <img width="731" alt="diffeomorphic_registration" src="https://user-images.githubusercontent.com/46209868/184736645-c809e26f-736b-441f-bdfc-c5ccb1d122fd.png">
----
1. AtlasImgMedian25.mhd had a DimSize that was 25% of the original size, which sometimes affected the output of affine-aligned images.
2. Input to both "larvalign" and "voxelmorph" are scaled down versions of the affine-aligned images.
3. "larvalign" nonlinear-registered results are same as that in Setup_2.
4. Due to space constraint.
