console.log('Client-side JavaScript is running');

const todosButton = document.getElementById('todos-button');

todosButton.addEventListener('click', () => {
    fetch('/todos?count=5')
        .then(response => response.json())
        .then(data => {
            const todosList = document.getElementById('todos-table-body');
            todosList.innerHTML = '';
            data.forEach(todo => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${todo.id}</td>
                    <td>${todo.title}</td>
                    <td>${todo.completed}</td>
                `;
                todosList.appendChild(row);
            });
        });
});