### Use this as template to create whatever collection you need

This module provides a generic way to interact with any MongoDB collection.

#### Implementation Steps:

1. **Model**: Create the model in the `models` folder.
2. **Repository**: Create the repository in the `repositories` folder.
   - **Important**: Change the `col_name` variable to match your MongoDB collection name.
3. **Controller**: Create the controller in the `controller` folder.
4. **Integration**: Add the controller to the `main.py` file.

### Steps for future. 

right now depends in the method execute_operation, everything is implemented here, even method to cast _id to ObjectId and vice versa. 
that problably will be moved to dataclouder_mongo, so will be easy to reuse. 

#### Generic Database Operations

The `execute_operation` method in the repository is designed to accept various MongoDB actions through a single endpoint. It supports:

- `findOne`: Retrieve a single document.
- `find`: Retrieve multiple documents.
- `create`: Insert one or many documents.
- `updateOne` / `updateMany`: Modify existing documents.
- `deleteOne`: Remove a single document.
- `aggregate`: Run complex aggregation pipelines.

> [!TIP]
> The utility functions automatically handle `_id` casting. If you provide an `_id` as a string in your query, it will be automatically converted to a MongoDB `ObjectId` before execution.
