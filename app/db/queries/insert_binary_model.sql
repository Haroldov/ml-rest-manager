INSERT INTO ml_binary_model (model_id, model) VALUES(%s, _binary %s) AS new_row
ON DUPLICATE KEY UPDATE model = new_row.model
