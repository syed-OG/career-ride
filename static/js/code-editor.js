document.addEventListener('DOMContentLoaded', function() {
    // Initialize code editor if the element exists
    const codeEditorElement = document.getElementById('code-editor');
    if (codeEditorElement) {
        // Initialize CodeMirror
        const editor = CodeMirror.fromTextArea(codeEditorElement, {
            mode: 'python',
            theme: 'monokai',
            lineNumbers: true,
            indentUnit: 4,
            lineWrapping: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            styleActiveLine: true,
            extraKeys: {
                "Tab": function(cm) {
                    var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
                    cm.replaceSelection(spaces);
                }
            }
        });
        
        // Adjust editor height
        editor.setSize(null, 400);
        
        // Language selection changes the editor mode
        const languageSelect = document.getElementById('language');
        if (languageSelect) {
            languageSelect.addEventListener('change', function() {
                const language = this.value;
                let mode;
                
                switch (language) {
                    case 'python':
                        mode = 'python';
                        break;
                    case 'javascript':
                        mode = 'javascript';
                        break;
                    case 'java':
                        mode = 'text/x-java';
                        break;
                    case 'cpp':
                        mode = 'text/x-c++src';
                        break;
                    default:
                        mode = 'python';
                }
                
                editor.setOption('mode', mode);
            });
        }
        
        // When form is submitted, update the hidden textarea
        const solutionForm = document.querySelector('#solution-form');
        if (solutionForm) {
            solutionForm.addEventListener('submit', function() {
                editor.save();
            });
        }
        
        // Run code button functionality
        const runButton = document.getElementById('run-code');
        const outputDiv = document.getElementById('code-output');
        
        if (runButton && outputDiv) {
            runButton.addEventListener('click', function() {
                const code = editor.getValue();
                const language = document.getElementById('language').value;
                
                outputDiv.innerHTML = '<div class="alert alert-info">Running your code...</div>';
                
                // In a real application, this would send the code to a backend service
                // For this demo, we'll simulate code execution
                setTimeout(function() {
                    outputDiv.innerHTML = '<div class="alert alert-success"><strong>Code ran successfully!</strong><br>This is a simulation. In a real app, your code would be executed securely on the server.</div>';
                }, 1500);
            });
        }
        
        // Load previous solutions if available
        const solutionSelect = document.getElementById('previous-solutions');
        if (solutionSelect) {
            solutionSelect.addEventListener('change', function() {
                const solutionId = this.value;
                if (solutionId) {
                    // In a real app, this would fetch the solution from the server
                    // For now, we'll use the data attributes on the select option
                    const selectedOption = this.options[this.selectedIndex];
                    const code = selectedOption.dataset.code;
                    const language = selectedOption.dataset.language;
                    
                    if (code) {
                        editor.setValue(code);
                    }
                    
                    if (language && languageSelect) {
                        languageSelect.value = language;
                        languageSelect.dispatchEvent(new Event('change'));
                    }
                }
            });
        }
    }
    
    // Initialize example buttons
    const showExampleButtons = document.querySelectorAll('.show-example-btn');
    if (showExampleButtons) {
        showExampleButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const exampleId = this.dataset.target;
                const exampleElement = document.getElementById(exampleId);
                
                if (exampleElement) {
                    if (exampleElement.style.display === 'none' || !exampleElement.style.display) {
                        exampleElement.style.display = 'block';
                        this.textContent = 'Hide Example';
                    } else {
                        exampleElement.style.display = 'none';
                        this.textContent = 'Show Example';
                    }
                }
            });
        });
    }
});
