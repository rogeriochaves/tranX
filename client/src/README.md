# Guiding code styles

- Use named functions instead of anonymous because they are more helpful when debugging
- Elm-UI concept of Rows and Cols as foundation for building the UI
- Elm styled-components (pre-elm ui) idea of keeping stylesheets only for STYLE, padding, margin, width, height etc is forbidden there, positioning attributes should be inline on the react componentes, because they are very coupled with markup
- Tests should not know much about implementation details, allowing for refactor on the code without the need to change the tests, Sociable not Solitary tests (check Martin Fowler definition)
- Strong types, any is not allowed, but also don't go crazy about typing
- Life of a file by Evan Czaplicki, it's okay to have big file components, it should be easy to refactor later
- I'm already ashamed of the amount of libraries I'm using in package.json, think twice before addind a new dependency
