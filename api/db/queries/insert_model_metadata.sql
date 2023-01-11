INSERT INTO ml_metadata (
  model_id, model_type, init_params, num_classes, num_features, num_training
) VALUES(%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE num_training = num_training + 1
