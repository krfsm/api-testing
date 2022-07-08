(function() {
"use strict";

// get the element to put the result in.
const content = document.getElementById("content");

function showResults() {
	// we iterate over the result array
	for (let i = 0; i < DATA.length; i++) {
    	var result = DATA[i];

		// create element and text node with the test case
		var testName = document.createElement("div");
		var testNameText = document.createTextNode('test case: ' + Object.keys(result)[0]);
		// and set all the attributes and such
		testName.setAttribute("id", "testCase" + i);
		testName.appendChild(testNameText);
		content.appendChild(testName);
		// same for the status
		var status = document.createElement("div");
		var statusText = document.createTextNode(Object.values(result)[0]);
		status.setAttribute("id", "testCase" + i + "status");
		status.appendChild(statusText);
		testName.appendChild(status);
		// and then set the attribute for status
		switch(Object.values(result)[0]) {
			case 'failure':
				testName.setAttribute("class", "failure");
				break;
			case 'success':
				testName.setAttribute("class", "success");
				break;
			default:
				testName.setAttribute("class", "failure");
		};
	};
};

showResults();

})();