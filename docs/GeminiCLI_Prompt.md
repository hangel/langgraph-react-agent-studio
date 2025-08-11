# [I have been testing and using Gemini CLI in the last weeks. Here's what my setup looks like](https://x.com/_philschmid/status/1937887668710355265)

# For complex tasks, I *never* ask for code first. 

*  My initial prompt is to create a plan 
     "Create a detailed implementation plan for [FEATURE, BUG]".
* Create multiple hierarchical GEMINI md files defining 
  * roles
  * helpful code snippets
  * a strict rule: "You cannot edit this file."
* Collaboration >> YOLO. I don't use a "YOLO mode" and rather intercept and re-prompt.
* Use MCP servers to access 
  * bugs
  * issues
  * browsers
  * Github (& internal tools)
  * run code in sandboxes.
* Leverage the 1M Context. Instruct it to read a lot of files into context or use “@” primitives.
* Code → Test → Commit. I force it to write tests or execute code snippets and have it fix it in a loop.

