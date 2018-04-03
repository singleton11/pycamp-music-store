=================================
Javascript Documentation Standard
=================================

The following is the Saritasa guideline how the JavaScript code should be documented by Python/Frontend teams

What Should Be Documented
=================================

The following is a list of what should be documented in our JavaScript files:

- Functions and it's arguments
- Class and it's methods
- Objects and it's properties
- Requires
- File headers

Documenting Tips
=================================

Short descriptions should be clear, simple, and brief. Document “what” and “when” – “why” should rarely need to be included. For example:

.. attention:: **Important**

   Functions and closures are third-person singular elements, meaning third-person singular verbs should be used to describe what each does. The documentation should answer the question "What it does?", therefore (It) 'Adds a click event on form dom element' is a good documentation as clearly answer the question.

**Functions:** What does the function do?

- **Good**: Handles a click on X element.
- **Bad**: Included for back-compat for X element. (It) included...- incorrect english


Functions
=================================

Functions should be formatted as follows:

- **Long description:** A supplement to the short description, providing a more detailed description. Use a period at the end.
- **@summary:** Short description – a brief, one line explanation of the purpose of the function. Use a period at the end.
- **@deprecated x.x.x:** Only use for deprecated functions, and provide the version the function was deprecated which should always be 3-digit (e.g. @since 3.6.0), and the function to use instead.
- **@since x.x.x:** Should always be 3-digit (e.g. @since 3.6.0).
- **@see:** A function or class relied on.
- **@link:** URL that provides more information.
- **@fires:** Event fired by the function.
- **@listens:** Events this function listens for.
- **@global:** List JavaScript globals that are used within the function, with an optional description of the global.
- **@param:** Give a brief description of the variable; denote particulars (e.g. if the variable is optional, its default) with JSDoc @param syntax.
- **@returns:** Note the period after the description.

An example::

 /**
  * @summary Short description. (use period)
  *
  * Long. (use period)
  *
  * @since x.x.x
  * @deprecated x.x.x Use new_function_name() instead.
  * @access private
  *
  * @class
  * @augments superclass
  * @mixes mixin
  *
  * @see Function/class relied on
  * @link URL
  * @global type $varname Short description.
  * @fires target:event
  * @listens target:event
  *
  * @param type $var Description.
  * @param type $var Optional. Description.
  * @returns type Description.
  */

.. attention:: **@summary vs Long descriptions**

   If you have no long description, then `@summary` is not needed, just write a short explanation of the
   function. Keep in mind that `@summary` if defined, should be always on top of the function comment block
   as shown above



Object Properties
=================================

Object properties should be formatted as follows:

- **Short description:** Use a period at the end.
- **@since x.x.x:** Should always be 3-digit (e.g. @since 3.6.0).
- **@access:** If the property is private, protected or public. Private properties are intended for internal use only.
- **@property:** Formatted the same way as @param.

An example::

 /**
  * Short description. (use period)
  *
  * @since x.x.x
  * @access (private, protected, or public)
  * @property type $var Description.
  */


File Headers
=================================

The JSDoc file header block is used to give an overview of what is contained in the file.

Whenever possible, all JavaScript files should contain a header block.

Files or libraries required should be documented with a short description JSDoc block using the @requires tag.

An example::

 /**
  * The long description of the file's purpose goes here and
  * describes in detail the complete functionality of the file.
  * This description can span several lines and ends with a period.
  *
  * @summary   A short description of the file.
  *
  * @link      URL
  * @since     x.x.x (if available)
  * @requires axios.js, alertify.js
  */


.. attention:: **@summary vs Long descriptions**

   If you have no long description, then `@summary` is not needed, just write a short explanation of the
   file/module. Keep in mind that `@summary` if defined, should be below the long description in the comment block
   as shown above (this is different for functions, where `@summary` should be at the top)

Supported JSDoc Tags
=================================

We may use the following JSDoc tags in our comment blocks.

============  ==========================================================================
Tag           Description
============  ==========================================================================
@abstract     This method can be implemented (or overridden) by the inheritor.
@access       Specify the access level of this member (private, public, or protected).
@author       Identify the author of an item.
@callback     Document a callback function.
@class        This function is a class constructor.
@classdesc    Use the following text to describe the entire class.
@constant     Document an object as a constant.
@copyright    Document some copyright information.
@default      Document the default value.
@deprecated   Document that this is no longer the preferred way.
@description  Describe a symbol.
@enum         Document a collection of related properties.
@event        Document an event.
@example      Provide an example of how to use a documented item.
@exports      Identify the member that is exported by a JavaScript module.
@external     Document an external class/namespace/module.
@file         Describe a file.
@fires        Describe the events this method may fire.
@function     Describe a function or method.
@global       Document a global object.
@link         Inline tag – create a link.
@mixin        Document a mixin object.
@module       Document a JavaScript module.
@name         Document the name of an object.
@namespace    Document a namespace object.
@param        Document the parameter to a function.
@private      This symbol is meant to be private.
@property     Document a property of an object.
@protected    This member is meant to be protected.
@public       This symbol is meant to be public.
@readonly     This symbol is meant to be read-only.
@requires     This file requires a JavaScript module.
@returns      Document the return value of a function.
@see          Refer to some other documentation for more information.
@since        When was this feature added?
@static       Document a static member.
@summary      A shorter version of the full description.
@this         What does the ‘this’ keyword refer to here?
@throws       Describe what errors could be thrown.
@todo         Document tasks to be completed.
@tutorial     Insert a link to an included tutorial file.
@type         Document the type of an object.
@typedef      Document a custom type.
@variation    Distinguish different objects with the same name.
@version      Documents the version number of an item.
============  ==========================================================================



Unsupported JSDoc Tags
=================================

We should not use the following JSDoc tags in our comment blocks as their aliases
for other tags.

=============  ==========================================================================
Tag            Description
=============  ==========================================================================
@virtual       An unsupported synonym. Use @abstract instead.
@constructor   An unsupported synonym. Use @class instead.
@const         An unsupported synonym. Use @constant instead.
@defaultvalue  An unsupported synonym. Use @default instead.
@desc          An unsupported synonym. Use @description instead.
@host          An unsupported synonym. Use @external instead.
@fileoverview  An unsupported synonym. Use @file instead.
@overview      An unsupported synonym. Use @file instead.
@emits         An unsupported synonym. Use @fires instead.
@func          An unsupported synonym. Use @function instead.
@method        An unsupported synonym. Use @function instead.
@var           An unsupported synonym. Use @member instead.
@emits         An unsupported synonym. Use @fires instead.
@arg           An unsupported synonym. Use @param instead.
@argument      An unsupported synonym. Use @param instead.
@prop          An unsupported synonym. Use @property instead.
@return        An unsupported synonym. Use @returns instead.
@exception     An unsupported synonym. Use @throws instead.
=============  ==========================================================================
