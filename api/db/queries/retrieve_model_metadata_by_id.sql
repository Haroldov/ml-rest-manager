SELECT
  model,
  model_type,
  init_params,
  num_classes,
  num_features,
  num_training
FROM db.ml_metadata m
INNER JOIN db.ml_binary_model b on b.model_id = m.model_id
WHERE b.model_id = %s
