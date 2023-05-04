/**
 * Load table of inputs for given sizes
 * @param { int } size
 */
function loadTable(size) {
  const table = document.getElementById('graphTable');
  table.innerHTML = '';

  const header = table.createTHead();
  const headerRow = header.insertRow(0);
  for (let i = 0; i < size + 1; i++) {
    headerRow.insertCell(i).innerHTML = i === 0 ? '' : `${i - 1}`;
  }


  for (let i = 0; i < size; i++) {
    const tableRow = table.insertRow();

    for (let j = 0; j < size + 1; j++) {
      if (j === 0) {
        tableRow.insertCell(j).innerHTML = `${i}`;
      } else {
        tableRow.insertCell(j).innerHTML = `
          <input type="number"
                 onfocus="this.style.backgroundColor='initial'"
                 onkeyup="inputOnChange(this, ${i}, ${j - 1}, ${size})" 
                 ${i === j - 1 ? 'value="0" readonly' : ''}
                 ${i < j - 1 ? 'tabindex=0' : 'tabindex=-1'}>
        `;
      }
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
  const inputs = document.querySelectorAll('input:not(#graphPointsCount)');
  for (const input of inputs) {
    if (input.value === '') {
      input.style.backgroundColor = 'lightcoral';
      return;
    }
  }

  const xhr = new XMLHttpRequest();

  xhr.open('POST', '/solve');
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.send(
    JSON.stringify({
      points: getGraphContent()
    })
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

/**
 * Fill symmetric table field then input content changes
 * @param { Object } instance
 * @param { int } i
 * @param { int } j
 * @param { int } size
 */
function inputOnChange(instance, i, j, size) {
  const inputs = document.querySelectorAll('input:not(#graphPointsCount)');

  inputs.forEach(
    (input) => input.getAttribute('name') !== 'size'
      ? inputs[size * j + i].value = instance.value
      : null
  )
}