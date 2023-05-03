/** Load table of inputs for given sizes */
function loadTable(size) {
  const table = document.getElementById('graphTable');
  table.innerHTML = '';

  const header = table.createTHead();
  const headerRow = header.insertRow(0);
  for (let i = 0; i < size + 1; i++) {
    headerRow.insertCell(i).innerHTML = i === 0 ? '' : `${i}`;
  }


  for (let i = 0; i < size; i++) {
    const tableRow = table.insertRow();

    for (let j = 0; j < size + 1; j++) {
      if (j === 0) tableRow.insertCell(j).innerHTML = `${i + 1}`;
      else tableRow.insertCell(j).innerHTML = '<input type="text">';
    }
  }

  const buttonContainer = document.getElementById('submitButtonContainer');
  buttonContainer.innerHTML = '<button type="submit" onclick="solveVRP()">Solve</button>';
}

/** Collect data from table */
function getGraphContent() {
  const inputs = [];

  document.querySelectorAll('tr:not(:first-child)').forEach(
    function (element) {
      inputs.push([]);
      element.querySelectorAll('td > input').forEach(
        (element) => inputs.at(-1).push(parseFloat(element.value ?? '0'))
      );
    }
  );

  return inputs;
}

/** Request for VRP problem solution */
function solveVRP() {
  const xhr = new XMLHttpRequest();

  xhr.open('POST', '/solve');
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.send(
    JSON.stringify(
      {
        points: getGraphContent()
      }
    )
  );

  xhr.onreadystatechange = function (response) {
    if (xhr.readyState === 4) {
      const responseJson = JSON.parse(xhr.responseText);
      console.log(responseJson);

      const answerContainer = document.getElementById('answerContainer');
      answerContainer.innerHTML = `<h3>The shortest path is: ${responseJson['path']}</h3>`
      answerContainer.innerHTML += `<h3>The shortest path length is: ${responseJson['length']}</h3>`
    }
  }
}