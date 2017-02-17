var editor = CodeMirror.fromTextArea(document.getElementById("code_editor"), {
	lineNumbers: true,
	styleActiveLine: true,
	matchBrackets: true,
	indentUnit: 4,
	tabSize: 4,
	theme: 'monokai',
	keyMap: 'sublime',
	autoCloseBrackets: true,
	styleActiveLine: true,
	extraKeys: {
		"Alt-F": "findPersistent",
		"F11": function(cm) {
			cm.setOption("fullScreen", !cm.getOption("fullScreen"));

        },
        "Esc": function(cm) {
        	
        	if (cm.getOption("fullScreen"))
        	{
        		cm.setOption("fullScreen", false);
        	}
        }
    },
	mode: {name: "javascript", globalVars: true}
  });

var is_vim_on = false;
var vim_elmt = document.getElementById('toggle_vim');

var editor_element = document.getElementsByClassName('CodeMirror')[0];

var text_size = 16;

editor_element.style.fontSize = text_size;

function selectTheme(input)
{
	//var input = document.getElementById('select');

	var theme = input.options[input.selectedIndex].textContent;
	
	var url = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.21.0/theme/'+ theme +'.css';

	var links = $('link[href="' + url +'"]');
	
	if(links.length == 0)
	{
		// document doesn't have the required theme.css file

		var theme_css = document.createElement('link');

		theme_css.setAttribute("rel", "stylesheet");
        theme_css.setAttribute("type", "text/css");
        theme_css.setAttribute("href", 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.21.0/theme/'+ theme +'.css');
		
		theme_css.onload = function () {
			editor.setOption("theme", theme);			
		};

		document.head.appendChild(theme_css);
	}
	else
	{
		editor.setOption("theme", theme);
	}

}

function changeFontSize (type) {
	text_size += type;
	editor_element.style.fontSize = text_size;
}

function toggleVimMode()
{
	if(is_vim_on)
	{
		is_vim_on = false;
		editor.setOption("keyMap", 'sublime');
		vim_elmt.innerHTML = "Enable vim mode";
	}
	else
	{
		is_vim_on = true;
		editor.setOption("keyMap", 'vim');
		vim_elmt.innerHTML = "Enable sublime mode";
	}
}