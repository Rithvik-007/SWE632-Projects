/**
 * @jest-environment jsdom
 */
jest.useFakeTimers(); // Use fake timers for the typeAnimation delays.

function typeAnimation(text, element, callback) {
  let index = 0;
  element.value = ""; // Clear current content.
  function type() {
    if (index < text.length) {
      element.value += text.charAt(index);
      index++;
      setTimeout(type, 50); // Typing delay.
    } else if (callback) {
      callback();
    }
  }
  type();
}

describe("Component Generator", () => {
  beforeEach(() => {
    // Set up a minimal DOM for testing.
    document.body.innerHTML = `
      <div>
        <input type="text" id="component-input" />
        <button id="generate-btn">Generate</button>
        <textarea id="code-editor"></textarea>
        <iframe id="output"></iframe>
      </div>
    `;

    // Make jQuery available globally.
    global.$ = require("jquery");

    // Stub $.getJSON to immediately call its callback with our test data.
    $.getJSON = jest.fn((url, callback) => {
      const data = {
        login: "Test Login Code",
        shopping_cart: "Test Shopping Cart Code"
      };
      callback(data);
    });

    // Attach the click event handler as in the production code.
    $("#generate-btn").click(function() {
      let inputVal = $("#component-input").val().trim().toLowerCase();
      // Replace spaces with underscores.
      inputVal = inputVal.replace(" ", "_");
      $.getJSON("codeSnippets.json", function(data) {
        if (inputVal !== "login" && inputVal !== "shopping_cart") {
          alert("No specific code is available for the given component");
          return;
        }
        const code = data[inputVal] ? data[inputVal].replace(/\\n/g, "\n") : "";
        if (code) {
          typeAnimation(code, document.getElementById("code-editor"), function() {
            // Callback after typing completes.
          });
          $("#code-editor").prop("readonly", true);
        }
      });
    });
  });

  test("populates code editor with login snippet on generate button click", () => {
    // Set input to "login".
    document.getElementById("component-input").value = "login";
    // Simulate button click.
    document.getElementById("generate-btn").click();
    // Fast-forward all timers to complete typeAnimation.
    jest.runAllTimers();
    // Verify that the code editor received the login snippet.
    expect(document.getElementById("code-editor").value).toBe("Test Login Code");
  });

  test("populates code editor with shopping_cart snippet on generate button click", () => {
    // Set input to "shopping_cart".
    document.getElementById("component-input").value = "shopping_cart";
    document.getElementById("generate-btn").click();
    jest.runAllTimers();
    expect(document.getElementById("code-editor").value).toBe("Test Shopping Cart Code");
  });

  test("alerts error for invalid component input", () => {
    // Spy on window.alert.
    const alertSpy = jest.spyOn(window, "alert").mockImplementation(() => {});
    // Set input to an invalid component.
    document.getElementById("component-input").value = "invalid";
    document.getElementById("generate-btn").click();
    // Verify that alert was called with the expected error message.
    expect(alertSpy).toHaveBeenCalledWith("No specific code is available for the given component");
    alertSpy.mockRestore();
  });
});
