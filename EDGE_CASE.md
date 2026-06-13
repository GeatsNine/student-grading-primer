# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation

Edge case: invalid or missing student mark

The primer states that the mark is optional when creating a student, but it does not fully specify how invalid marks should be handled.

If the mark is missing when creating a student, it defaults to 0.
If the mark is provided, it must be an integer.
The mark must be between 0 and 100.
If the mark is invalid, the API returns a 404 error response.

This keeps the API consistent with the primer requirement that errors return 404 and successful requests return 200. It also prevents invalid marks, such as negative marks or marks above 100, from being saved into the persistent database.