


//--------------------------------------------------
// DOM + XMLHttpRequest / Fetch + JSON + Timer API
//---------------------------------------------------

const top5TodosBtn = document.getElementById('top5-todos-btn');
const todosTbody = document.getElementById('todos-tbody');
const progressMessage = document.getElementById('progress-message');

top5TodosBtn.addEventListener('click', event => {
    const url = "https://jsonplaceholder.typicode.com/todos?_limit=5";
    const promise = fetch(url);
    promise
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(todos => {
            todosTbody.innerHTML = '';
            todos.forEach(todo => {
                const row = document.createElement('tr');
                const idCell = document.createElement('td');
                const titleCell = document.createElement('td');
                const completedCell = document.createElement('td');

                titleCell.textContent = todo.title;
                completedCell.textContent = todo.completed ? 'Yes' : 'No';

                row.appendChild(idCell);
                row.appendChild(titleCell);
                row.appendChild(completedCell);
                todosTbody.appendChild(row);
            });
        })
        .catch(error => {
            progressMessage.textContent = `Error fetching todos: ${error.message}`;
        });

});
