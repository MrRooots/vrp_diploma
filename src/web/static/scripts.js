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
    tableRow.setAttribute('id', 'adjacencyRow')

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

  document.getElementById('randomizeButtonContainer').innerHTML = `
    <button type="submit" onclick="fillRandomWeights()">Randomize</button>
  `;
}

/** Collect data from table */
function getGraphContent() {
  const inputs = [];

  document.querySelectorAll('tr[id="adjacencyRow"]').forEach(
    function (element) {
      inputs.push([]);
      element.querySelectorAll('td > input').forEach(
        (element) => inputs.at(-1).push(parseFloat(element.value ?? '0'))
      );
    }
  );
  console.log(inputs)
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
  const answerContainer = document.getElementById('answerContainer');
  const imageContainer = document.getElementById('imageContainer');
  answerContainer.innerHTML = '<h5 style="text-align: center; margin-bottom: 55px">Solution in progress, please wait...</h5>';
  imageContainer.innerHTML = '';

  const xhr = new XMLHttpRequest();

  xhr.open('POST', '/solve');
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.send(
    JSON.stringify({
      points: getGraphContent()
    })
  );

  xhr.onreadystatechange = function (_) {
    if (xhr.readyState === 4) {
      const responseJson = JSON.parse(xhr.responseText);

      answerContainer.innerHTML = `
        <table id="reportTable">
          <tr>
            <td id="reportTableLeftCell">Algorithm</td>
            <td>${responseJson['execution_report']['algorithm']}</td>
          </tr>
          <tr>
            <td id="reportTableLeftCell">Shortest path</td>
            <td>${responseJson['path']}</td>
          </tr>
          <tr>
            <td id="reportTableLeftCell">Length</td>
            <td>${responseJson['length']}</td>
          </tr>
          <tr>
            <td id="reportTableLeftCell">Execution time</td>
            <td>${responseJson['execution_report']['execution_time']} ms</td>
          </tr>
        </table>
      `;

      // Add image
      const image = new Image(640, 480);
      image.src = `data:image/png;base64,${responseJson['image']}`;
      imageContainer.innerHTML = '';
      imageContainer.append(image);
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

/** Fill all inputs with random values */
function fillRandomWeights() {
  const size = document.getElementById('graphPointsCount').value;
  const inputs = document.querySelectorAll('input:not(#graphPointsCount)');

  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      if (i < j) {
        inputs[size * i + j].value = Math.floor(Math.random() * (49) + 1);
        inputs[size * i + j].dispatchEvent(new Event('keyup'));
      }
    }
  }
}

/** Remove table, solution and image blocks */
function clearAll() {
  document.getElementById('graphTable').innerHTML = '';
  document.getElementById('submitButtonContainer').innerHTML = '';
  document.getElementById('graphPointsCount').value = '';
  document.getElementById('answerContainer').innerHTML = '';
  document.getElementById('imageContainer').innerHTML = '';
}

function terminateServer() {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/terminate');

  xhr.send(
    JSON.stringify({
      terminate: true
    })
  );


}