---
title: Chromium’s style guide
---

https://chromium.googlesource.com/chromium/src/+/refs/heads/main/styleguide/styleguide.md

# C++ Styleguide

This directory contains C++-specific pieces of Chromium's styleguide, including
the [guide itself](c++.md), a
[supplemental set of optional guidance](c++-dos-and-donts.md), and the list of
[allowed C++ language/library features](c++-features.md). To discuss anything in
here, email cxx@chromium.org or ask #cxx on Slack.

# Chromium C++ style guide

_For other languages, please see the
[Chromium style guides](https://chromium.googlesource.com/chromium/src/+/main/styleguide/styleguide.md)._

Chromium follows the [Google C++ Style
Guide](https://google.github.io/styleguide/cppguide.html) unless an exception
is listed below.

A checkout should give you
[clang-format](https://chromium.googlesource.com/chromium/src/+/main/docs/clang_format.md)
to automatically format C++ code. By policy, Clang's formatting of code should
always be accepted in code reviews.

You can propose changes to this style guide by sending an email to
`cxx@chromium.org`. Ideally, the list will arrive at some consensus and you can
request review for a change to this file. If there's no consensus,
`src/styleguide/c++/OWNERS` get to decide. For further details on how style
changes are handled and communicated, see the C++ Style Changes
[process documentation](https://chromium.googlesource.com/chromium/src/+/main/docs/process/c++_style_changes.md).

Blink code in `third_party/blink` uses [Blink style](blink-c++.md).

## Modern C++ features

Google and Chromium style
[targets C++20](https://google.github.io/styleguide/cppguide.html#C++_Version).
Additionally, some features of supported C++ versions remain forbidden. The
status of Chromium's C++ support is covered in more detail in
[Modern C++ use in Chromium](c++-features.md).

## Naming

  * "Chromium" is the name of the project, not the product, and should never
    appear in code, variable names, API names etc. Use "Chrome" instead.

## Tests and Test-only Code

  * Functions used only for testing should be restricted to test-only usages
    with the testing suffixes supported by
    [PRESUBMIT.py](https://chromium.googlesource.com/chromium/src/+/main/PRESUBMIT.py).
    `ForTesting` is the conventional suffix although similar patterns, such as
    `ForTest`, are also accepted. These suffixes are checked at presubmit time
    to ensure the functions are called only by test files. In the rare case of
    adding a test-only code path to an area where a testing suffix is not
    possible, CHECK_IS_TEST() may be appropriate.
  * Classes used only for testing should be in a GN build target that is
    marked `testonly=true`. Tests can depend on such targets, but production
    code can not.
  * While test files generally appear alongside the production code they test,
    support code for `testonly` targets should be placed in a `test/` subdirectory.
    For example, see `//mojo/core/core_unittest.cc` and
    `//mojo/core/test/mojo_test_base.cc`. For test classes used across multiple
    directories, it might make sense to move them into a nested `test` namespace for
    clarity.
  * Despite the Google C++ style guide
    [deprecating](https://google.github.io/styleguide/cppguide.html#File_Names)
    the `_unittest.cc` suffix for unit test files, in Chromium we still use this
    suffix to distinguish unit tests from browser tests, which are written in
    files with the `_browsertest.cc` suffix.

## Code formatting

  * Put `*` and `&` by the type rather than the variable name.
  * In class declarations, group function overrides together within each access
    control section, with one labeled group per parent class.
  * Prefer `(foo == 0)` to `(0 == foo)`.
  * Use `{}` on all conditionals/loops.

## Unnamed namespaces

Items local to a .cc file should be wrapped in an unnamed namespace. While some
such items are already file-scope by default in C++, not all are; also, shared
objects on Linux builds export all symbols, so unnamed namespaces (which
restrict these symbols to the compilation unit) improve function call cost and
reduce the size of entry point tables.

## Exporting symbols

Symbols can be exported (made visible outside of a shared library/DLL) by
annotating with a `<COMPONENT>_EXPORT` macro name (where `<COMPONENT>` is the
name of the component being built, e.g. BASE, NET, CONTENT, etc.). Class
annotations should precede the class name:
```c++
class FOO_EXPORT Foo {
  void Bar();
  void Baz();
  // ...
};
```

Function annotations should precede the return type:
```c++
class FooSingleton {
  FOO_EXPORT Foo& GetFoo();
  FOO_EXPORT Foo& SetFooForTesting(Foo* foo);
  void SetFoo(Foo* foo);  // Not exported.
};
```

## Multiple inheritance

Multiple inheritance and virtual inheritance are permitted in Chromium code,
but discouraged (beyond the "interface" style of inheritance allowed by the
Google style guide, for which we do not require classes to have the "Interface"
suffix). Consider whether composition could solve the problem instead.

## Inline functions

Simple accessors should generally be the only inline functions. These should be
named using `snake_case()`. Virtual functions should never be declared this way.

## Logging

Remove all logging before checking in code. The exception is temporary logging
to track down a specific bug. This should be a rare exception, and you should
have a plan for how to manually collect/use the logged data. Afterwards you
should remove the logging. Note that logs are not present in crashes. Use
`base::debug::ScopedCrashKeyString`
([link](https://chromium.googlesource.com/chromium/src/+/main/base/debug/crash_logging.h))
for that.

For the rare case when logging needs to stay in the codebase for a while,
prefer `DVLOG(1)` to other logging methods. This avoids bloating the release
executable and in debug can be selectively enabled at runtime by command-line
arguments:
  * `--v=n` sets the global log level to n (default 0). All log statements with
    a log level less than or equal to the global level will be printed.
  * `--vmodule=mod=n[,mod=n,...]` overrides the global log level for the module
    mod. Supplying the string foo for mod will affect all files named foo.cc,
    while supplying a wildcard like `*bar/baz*` will affect all files with
    `bar/baz` in their full pathnames.

Rationale:
* Logging is expensive: binary size, runtime.
* Logging quickly loses utility as more components emit logs: too much noise,
  not enough signal.
* Logging is often used to document impossible edge cases which should be
  enforced with CHECKs. The latter makes it easier to reason about the code, and
  can result in more performant binaries.

## Platform-specific code

To `#ifdef` code for specific platforms, use the macros defined in
`build/build_config.h` and in the Chromium build config files, not other macros
set by specific compilers or build environments (e.g. `WIN32`).

Place platform-specific #includes in their own section below the "normal"
`#includes`. Repeat the standard `#include` order within this section:

```c++
  #include "foo/foo.h"

  #include <stdint.h>
  #include <algorithm>

  #include "base/strings/utf_string_conversions.h"
  #include "build/build_config.h"
  #include "chrome/common/render_messages.h"

  #if BUILDFLAG(IS_WIN)
  #include <windows.h>
  #include "base/win/com_init_util.h"
  #elif BUILDFLAG(IS_POSIX)
  #include "base/posix/global_descriptors.h"
  #endif
```

## Types

  * Refer to the [Mojo style
    guide](https://chromium.googlesource.com/chromium/src/+/main/docs/security/mojo.md)
    when working with types that will be passed across network or process
    boundaries. For example, explicitly-sized integral types must be used for
    safety, since the sending and receiving ends may not have been compiled
    with the same sizes for things like `int` and `size_t`.
  * Use `size_t` for object and allocation sizes, object counts, array and
    pointer offsets, vector indices, and so on. This prevents casts when
    dealing with STL APIs, and if followed consistently across the codebase,
    minimizes casts elsewhere.
  * Occasionally classes may have a good reason to use a type other than
    `size_t` for one of these concepts, e.g. as a storage space optimization. In
    these cases, continue to use `size_t` in public-facing function
    declarations, and continue to use unsigned types internally (e.g.
    `uint32_t`).
  * Follow the [integer semantics
    guide](https://chromium.googlesource.com/chromium/src/+/main/docs/security/integer-semantics.md)
    for all arithmetic conversions and calculations used in memory management
    or passed across network or process boundaries. In other circumstances,
    follow [Google C++ casting
    conventions](https://google.github.io/styleguide/cppguide.html#Casting)
    to convert arithmetic types when you know the conversion is safe. Use
    `checked_cast<T>` (from `base/numerics/safe_conversions.h`) when you need to
    `CHECK` that the source value is in range for the destination type. Use
    `saturated_cast<T>` if you instead wish to clamp out-of-range values.
    `CheckedNumeric` is an ergonomic way to perform safe arithmetic and casting
    in many cases.
  * The Google Style Guide [bans
    UTF-16](https://google.github.io/styleguide/cppguide.html#Non-ASCII_Characters).
    For various reasons, Chromium uses UTF-16 extensively. Use `std::u16string`
    and `char16_t*` for 16-bit strings, `u"..."` to declare UTF-16 literals, and
    either the actual characters or the `\uXXXX` or `\UXXXXXXXX` escapes for
    Unicode characters. Avoid `\xXX...`-style escapes, which can cause subtle
    problems if someone attempts to change the type of string that holds the
    literal. In code used only on Windows, it may be necessary to use
    `std::wstring` and `wchar_t*`; these are legal, but note that they are
    distinct types and are often not 16-bit on other platforms.

## Object ownership and calling conventions

When functions need to take raw or smart pointers as parameters, use the
following conventions. Here we refer to the parameter type as `T` and name as
`t`.
  * If the function does not modify `t`'s ownership, declare the param as `T*`.
    The caller is expected to ensure `t` stays alive as long as necessary,
    generally through the duration of the call. Exception: In rare cases (e.g.
    using lambdas with STL algorithms over containers of `unique_ptr<>`s), you
    may be forced to declare the param as `const std::unique_ptr<T>&`. Do this
    only when required.
  * If the function takes ownership of a non-refcounted object, declare the
    param as `std::unique_ptr<T>`.
  * If the function (at least sometimes) takes a ref on a refcounted object,
    declare the param as `scoped_refptr<T>`. The caller can decide
    whether it wishes to transfer ownership (by calling `std::move(t)` when
    passing `t`) or retain its ref (by simply passing t directly).
  * In short, functions should never take ownership of parameters passed as raw
    pointers, and there should rarely be a need to pass smart pointers by const
    ref.

Conventions for return values are similar with an important distinction:
  * Return raw pointers if-and-only-if the caller does not take ownership.
  * Return `std::unique_ptr<T>` or `scoped_refptr<T>` by value when the impl is
    handing off ownership.
  * **Distinction**: Return `const scoped_refptr<T>&` when the impl retains
    ownership so the caller isn't required to take a ref: this avoids bumping
    the reference count if the caller doesn't need ownership and also
    [helps binary size](https://crrev.com/c/1435627)).

A great deal of Chromium code predates the above rules. In particular, some
functions take ownership of params passed as `T*`, or take `const
scoped_refptr<T>&` instead of `T*`, or return `T*` instead of
`scoped_refptr<T>` (to avoid refcount churn pre-C++11). Try to clean up such
code when you find it, or at least not make such usage any more widespread.

## Non-owning pointers in class fields

Use `const raw_ref<T>` or `raw_ptr<T>` for class and struct fields in place of a
raw C++ reference `T&` or pointer `T*` whenever possible, except in paths that include
`/renderer/` or `blink/public/web/`.  These are non-owning smart pointers that
have improved memory-safety over raw pointers and references, and can prevent
exploitation of a significant percentage of Use-after-Free bugs.

Prefer `const raw_ref<T>` whenever the held pointer will never be null, and it's
ok to drop the `const` if the internal reference can be reassigned to point to a
different `T`. Use `raw_ptr<T>` in order to express that the pointer _can_ be
null. Only `raw_ptr<T>` can be default-constructed, since `raw_ref<T>` disallows
nullness.

Using `raw_ref<T>` or `raw_ptr<T>` may not be possible in rare cases for
[performance reasons](../../base/memory/raw_ptr.md#Performance). Additionally,
`raw_ptr<T>` doesn’t support some C++ scenarios (e.g. `constexpr`, ObjC
pointers).  Tooling will help to encourage use of these types in the future. See
[raw_ptr.md](../../base/memory/raw_ptr.md#When-to-use-raw_ptr_T) for how to add
exclusions.

## thread_local variables

Much code in Chrome needs to be "sequence-aware" rather than "thread-aware". If
you need a sequence-local variable, see
[`base::SequenceLocalStorageSlot`](../../base/threading/sequence_local_storage_slot.h).

If you truly need a thread-local variable, then you can use a `thread_local`, as
long as it complies with the following requirements:
  * Its type must satisfy `std::is_trivially_destructible_v<T>`, due to past
    problems with "spooky action at a distance" during destruction. Note that
    `raw_ptr<T>` is not a trivially-destructible type and may not be contained
    in `thread_locals`.
  * It must not be exported (e.g. via `COMPONENT_EXPORT`), since this may result
    in codegen bugs on Mac; and at least on Windows, this probably won't compile
    in the component build anyway. As a workaround, create an exported getter
    function that creates a `thread_local` internally and returns a ref to it.
  * If it lives at class/namespace scope, it must be marked `ABSL_CONST_INIT`,
    as specified in
    [the Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html#thread_local).
  * It must not be constructed inside OOM handlers or any other code that cannot
    allocate memory, since on POSIX, construction may alloc.

If you can't comply with these requirements, consider
[`base::ThreadLocalOwnedPointer`](../../base/threading/thread_local.h) or
another nearby low-level utility.

## Forward declarations vs. #includes

Unlike the Google style guide, Chromium style prefers forward declarations to
`#includes` where possible. This can reduce compile times and result in fewer
files needing recompilation when a header changes.

You can and should use forward declarations for most types passed or returned
by value, reference, or pointer, or types stored as pointer members or in most
STL containers. However, if it would otherwise make sense to use a type as a
member by-value, don't convert it to a pointer just to be able to
forward-declare the type.

Headers that contain only forward declarations, such as
[`callback_forward.h`](../../base/functional/callback_forward.h), satisfy the
spirit of this rule. Note that the [Mojo bindings
generator](../../mojo/public/cpp/bindings/README.md#Getting-Started)
creates a `.mojom-forward.h` file along with every generated `.mojom.h` file
that can be included for forward declarations of Mojo types.

## File headers

All files in Chromium start with a common license header. That header should
look like this:

```c++
// Copyright $YEAR The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
```

Some important notes about this header:
  * `$YEAR` should be set to the current year at the time a file is created, and
    not changed thereafter.
  * For files specific to ChromiumOS, replace the word Chromium with the phrase
    ChromiumOS.
  * The Chromium project hosts mirrors of some upstream open-source projects.
    When contributing to these portions of the repository, retain the existing
    file headers.

Use standard `#include` guards in all header files (see the Google style guide
sections on these for the naming convention). Do not use `#pragma once`;
historically it was not supported on all platforms, and it does not seem to
outperform #include guards even on platforms which do support it.

## CHECK(), DCHECK() and NOTREACHED()

Use the `CHECK()` family of macros to both document and verify invariants.
  * Exception: If the invariant is known to be too expensive to verify in
    production, you may fall back to `DCHECK()`. Do not do this unless
    necessary.
  * Exception: If your pre-stable coverage is too small to prevent a stability
    risk once `CHECK()`s hit stable, and failure doesn't obviously result in a
    crash or security risk, you may use `CHECK(Foo(),
    base::NotFatalUntil::M120)` with a future milestone to gather non-fatal
    diagnostics in stable before automatically turning fatal in a later
    milestone.
  * Historically, Chromium code used `DCHECK()` in most cases, so a great deal
    of existing code uses `DCHECK()` instead of `CHECK()`. You are encouraged
    to migrate to `CHECK()`s with a trailing `base::NotFatalUntil::M120`
    argument, as there's stability risk given the under-tested invariant, or add
    a comment explaining why DCHECK is appropriate given the current guidance.

Use `NOTREACHED()` to indicate a piece of code is unreachable. Control flow does
not leave this call, so there should be no executable statements after it (even
return statements from non-void functions). The compiler will issue dead-code
warnings.
  * Prefer to unconditionally `CHECK()` instead of conditionally hitting a
    `NOTREACHED()`, where feasible.
  * Exception: If your pre-stable coverage is too small to prevent a stability
    risk once `NOTREACHED()`s hit stable, and failure doesn't obviously
    result in a crash or security risk, you may use `NOTREACHED(
    base::NotFatalUntil::M120)` with a future milestone to gather non-fatal
    diagnostics in stable before automatically turning fatal in a later
    milestone.

Use `base::ImmediateCrash()` in the rare case where it's necessary to terminate
the current process for reasons outside its control, that are not violations of
our invariants.

Use `base::debug::DumpWithoutCrashing()` to generate a crash report but keep
running in the case where you are investigating some failure but know that it's
safe to continue execution.

Use `DLOG(FATAL)` (does nothing in production) or `LOG(DFATAL)` (logs an error
and continues running in production) if you need to log an error in tests from
production code. From test code, use `ADD_FAILURE()` directly. Do not use these
for invariant failures. Those should use `CHECK()` or `NOTREACHED()` as noted
above.

For more details, see [checks.md](checks.md).

## Test-only code paths in production code

Try to avoid test-only code paths in production code. Such code paths make
production code behave differently in tests. This makes both tests and
production code hard to reason about. Consider dependency injection, fake
classes, etc to avoid such code paths.

However, if a test-only path in production code cannot be avoided, instrument
that code path with `CHECK_IS_TEST();` to assert that the code is only run in
tests.

```c++
// `profile_manager` may not be available in tests.
if (!profile_manager) {
  CHECK_IS_TEST();
  return std::string();
}
```

`CHECK_IS_TEST();` will crash outside of tests. This asserts that the test-only
code path is not accidentally or maliciously taken in production.

## Miscellany

  * Use UTF-8 file encodings and LF line endings.
  * Unit tests and performance tests should be placed in the same directory as
    the functionality they're testing.
  * The [C++ Dos and Don'ts](c++-dos-and-donts.md) page has more helpful
    information.

# C++ Dos and Don'ts

## A Note About Usage

Unlike the [style guide](c++.md), the content of this page is advisory, not
required. You can always deviate from something on this page, if the relevant
author/reviewer/OWNERS agree that another course is better.

## Minimize Code in Headers

* Remove #includes you don't use.  Unfortunately, Chromium lacks
  include-what-you-use ("IWYU") support, so there's no tooling to do this
  automatically.  Look carefully when refactoring.
* Where possible, forward-declare nested classes, then give the full declaration
  (and definition) in the .cc file.
* Defining a class method in the declaration is an implicit request to inline
  it.  Avoid this in header files except for cheap non-virtual getters and
  setters.  Note that constructors and destructors can be more expensive than
  they appear and should also generally not be inlined.

## Static variables

Dynamic initialization of function-scope static variables is **thread-safe** in
Chromium (per standard C++11 behavior). Before 2017, this was thread-unsafe, and
base::LazyInstance was widely used. This is no longer necessary.
Background can be found in
[this thread](https://groups.google.com/a/chromium.org/forum/#!msg/chromium-dev/p6h3HC8Wro4/HHBMg7fYiMYJ)
and
[this thread](https://groups.google.com/a/chromium.org/d/topic/cxx/j5rFewBzSBQ/discussion).

```cpp
void foo() {
  static int ok_count = ComputeTheCount();  // OK; a problem pre-2017.
  static int good_count = 42;               // Done before dynamic initialization.
  static constexpr int better_count = 42;   // Even better (likely inlined at compile time).
  static auto& object = *new Object;        // For class types.
}
```

## Explicitly declare class copyability/movability

The
[Google Style Guide](http://google.github.io/styleguide/cppguide.html#Copyable_Movable_Types)
says classes can omit copy/move declarations or deletions "only if they are
obvious".  Because "obvious" is subjective and even the examples in the style
guide take some thought to figure out, being explicit is clear, simple, and
avoids any risk of accidental copying.

Declare or delete these operations in the public section, between other
constructors and the destructor; `DISALLOW_COPY_AND_ASSIGN` is deprecated.  For
a non-copyable/movable type, delete the copy operations (the move operations
will be implicitly deleted); otherwise, declare either copy operations, move
operations, or both (a non-declared pair will be implicitly deleted).  Always
declare or delete both construction and assignment, not just one (which can
introduce subtle bugs).

```cpp
class TypeName {
 public:
  TypeName(int arg);
  ...
  TypeName(const TypeName&) = delete;
  TypeName& operator=(const TypeName&) = delete;
  ...
  ~TypeName();
}
```

## Variable initialization

There are myriad ways to initialize variables in C++. Prefer the following
general rules:

1. Use assignment syntax when performing "simple" initialization with one or
   more literal values which will simply be composed into the object:

   ```cpp
   int i = 1;
   std::string s = "Hello";
   std::pair<bool, double> p = {true, 2.0};
   std::vector<std::string> v = {"one", "two", "three"};
   ```

   Using '=' here is no less efficient than "()" (the compiler won't generate a
   temp + copy), and ensures that only implicit constructors are called, so
   readers seeing this syntax can assume    nothing complex or subtle is
   happening.  Note that "{}" are allowed on the right side of the '=' here
   (e.g. when you're merely passing a set of initial values to a "simple"
   struct/   container constructor; see below items for contrast).
2. Use constructor syntax when construction performs significant logic, uses an
   explicit constructor, or in some other way is not intuitively "simple" to the
   reader:

   ```cpp
   MyClass c(1.7, false, "test");
   std::vector<double> v(500, 0.97);  // Creates 500 copies of the provided initializer
   ```
3. Use C++11 "uniform init" syntax ("{}" without '=') only when neither of the
   above work:

   ```cpp
   class C {
    public:
     explicit C(bool b) { ... };
     ...
   };
   class UsesC {
     ...
    private:
     C c{true};  // Cannot use '=' since C() is explicit (and "()" is invalid syntax here)
   };
   class Vexing {
    public:
     explicit Vexing(const std::string& s) { ... };
     ...
   };
   void func() {
     Vexing v{std::string()};  // Using "()" here triggers "most vexing parse";
                               // "{}" is arguably more readable than "(())"
     ...
   }
   ```
4. Never mix uniform init syntax with auto, since what it deduces is unlikely
   to be what was intended:

   ```cpp
   auto x{1};  // Until C++17, decltype(x) is std::initializer_list<int>, not int!
   ```

For more reading, please see abseil's [Tip of the Week #88: Initialization: =,
(), and {}](https://abseil.io/tips/88).

## Initialize members in the declaration where possible

If possible, initialize class members in their declarations, except where a
member's value is explicitly set by every constructor.

This reduces the chance of uninitialized variables, documents default values in
the declaration, and increases the number of constructors that can use
`=default` (see below).

```cpp
class C {
 public:
  C() : a_(2) {}
  C(int b) : a_(1), b_(b) {}

 private:
  int a_;          // Not necessary to init this since all constructors set it.
  int b_ = 0;      // Not all constructors set this.
  std::string c_;  // No initializer needed due to string's default constructor.
  base::WeakPtrFactory<C> factory_{this};
                   // {} allows calling of explicit constructors.
};
```

Note that it's possible to call functions or pass `this` and other expressions
in initializers, so even some complex initializations can be done in the
declaration.

## Use `std::make_unique` and `base::MakeRefCounted` instead of bare `new`

When possible, avoid bare `new` by using
[`std::make_unique<T>(...)`](http://en.cppreference.com/w/cpp/memory/unique_ptr/make_unique)
and
[`base::MakeRefCounted<T>(...)`](https://source.chromium.org/chromium/chromium/src/+/main:base/memory/scoped_refptr.h;l=98;drc=f8c5bd9d40969f02ddeb3e6c7bdb83029a99ca63):

```cpp
// BAD: bare call to new; for refcounted types, not compatible with one-based
// refcounting.
return base::WrapUnique(new T(1, 2, 3));
return base::WrapRefCounted(new T(1, 2, 3));

// BAD: same as the above, plus mentions type names twice.
std::unique_ptr<T> t(new T(1, 2, 3));
scoped_refptr<T> t(new T(1, 2, 3));
return std::unique_ptr<T>(new T(1, 2, 3));
return scoped_refptr<T>(new T(1, 2, 3));

// OK, but verbose: type name still mentioned twice.
std::unique_ptr<T> t = std::make_unique<T>(1, 2, 3);
scoped_refptr<T> t = base::MakeRefCounted<T>(1, 2, 3);

// GOOD; make_unique<>/MakeRefCounted<> are clear enough indicators of the
// returned type.
auto t = std::make_unique<T>(1, 2, 3);
auto t = base::MakeRefCounted<T>(1, 2, 3);
return std::make_unique<T>(1, 2, 3);
return base::MakeRefCounted<T>(1, 2, 3);
```

**Notes:**

1. Never friend `std::make_unique` to work around constructor access
   restrictions. It will allow anyone to construct the class. Use
   `base::WrapUnique` in this case.

   DON'T:
   ```cpp
   class Bad {
    public:
     std::unique_ptr<Bad> Create() { return std::make_unique<Bad>(); }
     // ...
    private:
     Bad();
     // ...
     friend std::unique_ptr<Bad> std::make_unique<Bad>();  // Lost access control
   };
   ```

   DO:
   ```cpp
   class Okay {
    public:
     // For explanatory purposes. If Create() adds no value, it is better just
     // to have a public constructor instead.
     std::unique_ptr<Okay> Create() { return base::WrapUnique(new Okay()); }
     // ...
    private:
     Okay();
     // ...
   };
   ```
2. `base::WrapUnique(new Foo)` and `base::WrapUnique(new Foo())` mean something
   different if `Foo` does not have a user-defined constructor. Don't make
   future maintainers guess whether you left off the '()' on purpose. Use
   `std::make_unique<Foo>()` instead. If you're intentionally leaving off the
   "()" as an optimization, please leave a comment.

   ```cpp
   auto a = base::WrapUnique(new A); // BAD: "()" omitted intentionally?
   auto a = std::make_unique<A>();   // GOOD
   // "()" intentionally omitted to avoid unnecessary zero-initialization.
   // base::WrapUnique() does the wrong thing for array pointers.
   auto array = std::unique_ptr<A[]>(new A[size]);
   ```

See also [TOTW 126](https://abseil.io/tips/126).

## Do not use `auto` to deduce a raw pointer

Do not use `auto` when the type would be deduced to be a pointer type; this can
cause confusion. Instead, specify the "pointer" part outside of `auto`:

```cpp
auto item = new Item();  // BAD: auto deduces to Item*, type of `item` is Item*
auto* item = new Item(); // GOOD: auto deduces to Item, type of `item` is Item*
```

## Use `const` correctly

For safety and simplicity, **don't return pointers or references to non-const
objects from const methods**. Within that constraint, **mark methods as const
where possible**.  **Avoid `const_cast` to remove const**, except when
implementing non-const getters in terms of const getters.

For more information, see [Using Const Correctly](const.md).

## Prefer to use `=default`

Use `=default` to define special member functions where possible, even if the
default implementation is just {}. Be careful when defaulting move operations.
Moved-from objects must be in a valid but unspecified state, i.e., they must
satisfy the class invariants, and the default implementations may not achieve
this.

```cpp
class Good {
 public:
  // We can, and usually should, provide the default implementation separately
  // from the declaration.
  Good();

  // Use =default here for consistency, even though the implementation is {}.
  ~Good() = default;
  Good(const Good& other) = default;

 private:
  std::vector<int> v_;
};

Good::Good() = default;
```

## Comment style

References to code in comments should be wrapped in `` ` ` `` pairs. Codesearch
uses this as a heuristic for finding C++ symbols in comments and generating
cross-references for that symbol. Historically, Chrome also used `||` pairs to
delimit variable names; codesearch understands both conventions and will
generate a cross-reference either way. Going forward, prefer the new style even
if existing code uses the old one.

* Class and type names: `` `FooClass` ``.
* Function names: `` `FooFunction()` ``. The trailing parens disambiguate
  against class names, and occasionally, English words.
* Variable names: `` `foo_var` ``.
* Tracking comments for future improvements: `// TODO(crbug.com/40781525): ...`,
  or, less optimally, `// TODO(knowledgeable_username): ...`.  Tracking bugs
  provide space to give background context and current status; a username might
  at least provide a starting point for asking about an issue.

```cpp
// `FooImpl` implements the `FooBase` class.
// `FooFunction()` modifies `foo_member_`.
// TODO(crbug.com/40097047): Rename things to something more descriptive than "foo".
```

## Named namespaces

Most code should be in a namespace, with the exception of code under
`//chrome`, which may be in the global namespace (do not use the `chrome::`
namespace). Minimize use of nested namespaces, as they do not actually
improve encapsulation; if a nested namespace is needed, do not reuse the
name of any top-level namespace. For more detailed guidance and rationale,
see https://abseil.io/tips/130.

## Guarding with DCHECK_IS_ON()

Any code written inside a `DCHECK()` macro, or the various `DCHECK_EQ()` and
similar macros, will be compiled out in builds where DCHECKs are disabled. That
includes any non-debug build where the `dcheck_always_on` GN arg is not present.

Thus even if your `DHECK()` would perform some expensive operation, you can
be confident that **code within the macro will not run in our official
release builds**, and that the linker will consider any function it calls to be
dead code if it's not used elsewhere.

However, if your `DCHECK()` relies on work that is done outside of the
`DCHECK()` macro, that work may not be eliminated in official release builds.
Thus any code that is only present to support a `DCHECK()` should be guarded by
`if constexpr (DCHECK_IS_ON())` (see the next item) or `#if DCHECK_IS_ON()` to
avoid including that code in official release builds.

This code is fine without any guards for `DCHECK_IS_ON()`.
```cpp
void ExpensiveStuff() { ... }  // No problem.

// The ExpensiveStuff() call will not happen in official release builds. No need
// to use checks for DCHECK_IS_ON() anywhere.
DCHECK(ExpensiveStuff());

std::string ExpensiveDebugMessage() { ... }  // No problem.

// Calls in stream operators are also dead code in official release builds (not
// called with the result discarded). This is fine.
DCHECK(...) << ExpensiveDebugMessage();
```

This code will probably do expensive things that are not needed in official
release builds, which is bad.
```cpp
// The result of this call is only used in a DCHECK(), but the code here is
// outside of the macro. That means it's likely going to show up in official
// release builds.
int c = ExpensiveStuff();  // Bad. Don't do this.
...
DCHECK_EQ(c, ExpensiveStuff());
```

Instead, any code outside of a `DCHECK()` macro, that is only needed when
DCHECKs are enabled, should be explicitly eliminated by checking
`DCHECK_IS_ON()` as this code does.
```cpp
// The result of this call is only used in a DCHECK(), but the code here is
// outside of the macro. We can't rely on the compiler to remove this in
// official release builds, so we should guard it with a check for
// DCHECK_IS_ON().
#if DCHECK_IS_ON()
int c = ExpensiveStuff();  // Great, this will be eliminated.
#endif
...
#if DCHECK_IS_ON()
DCHECK_EQ(c, ExpensiveStuff());  // Must be guarded since `c` won't exist.
#endif
```

The `DCHECK()` and friends macros still require the variables and functions they
use to be declared at compile time, even though they will not be used at
runtime. This is done to avoid "unused variable" and "unused function" warnings
when DCHECKs are turned off. This means that you may need to guard the
`DCHECK()` macro if it depends on a variable or function that is also guarded
by a check for `DCHECK_IS_ON()`.

## Minimizing preprocessor conditionals

Eliminate uses of `#if ...` when there are reasonable alternatives. Some common
cases:

* APIs that are conceptually reasonable for all platforms, but only actually do
  anything on one. Instead of guarding the API and all callers in `#if`s, you
  can define and call the API unconditionally, and guard platform-specific
  implementation.
* Test code that expects different values under different `#define`s:
  ```cpp
    // Works, but verbose, and might be more annoying/prone to bugs during
    // future maintenance.
  #if BUILDFLAG(COOL_FEATURE)
    EXPECT_EQ(5, NumChildren());
  #else
    EXPECT_EQ(3, NumChildren());
  #endif

    // Shorter and less repetitive.
    EXPECT_EQ(BUILDFLAG(COOLFEATURE) ? 5 : 3, NumChildren());
  ```
* Code guarded by `DCHECK_IS_ON()` or a similar "should always work in either
  configuration" `#define`, which could still compile when the `#define` is
  unset. Prefer `if constexpr (DCHECK_IS_ON())` or similar, since the compiler
  will continue to verify the code's syntax in all cases, but it will not be
  compiled in if the condition is false. Note that this only works inside a
  function, and only if the code does not refer to symbols whose declarations
  are `#ifdef`ed away. Don't unconditionally declare debug-only symbols just
  to use this technique -- only use it when it doesn't require additional
  tweaks to the surrounding code.


# Modern C++ use in Chromium

_This document is part of the more general
[Chromium C++ style guide](https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++.md).
It summarizes the supported state of new and updated language and library
features in recent C++ standards and the [Abseil](https://abseil.io/about/)
library. This guide applies to both Chromium and its subprojects, though
subprojects can choose to be more restrictive if necessary for toolchain
support._

The C++ language has in recent years received an updated standard every three
years (C++11, C++14, etc.). For various reasons, Chromium does not immediately
allow new features on the publication of such a standard. Instead, once
Chromium supports the toolchain to a certain extent (e.g., build support is
ready), a standard is declared "_initially supported_", with new
language/library features banned pending discussion but not yet allowed.

You can propose changing the status of a feature by sending an email to
[cxx@chromium.org](https://groups.google.com/a/chromium.org/forum/#!forum/cxx).
Include a short blurb on what the feature is and why you think it should or
should not be allowed, along with links to any relevant previous discussion. If
the list arrives at some consensus, send a codereview to change this file
accordingly, linking to your discussion thread.

If an item remains on the TBD list two years after initial support is added,
style arbiters should explicitly move it to an appropriate allowlist or
blocklist, allowing it if there are no obvious reasons to ban.

The current status of existing standards and Abseil features is:

*   **C++11:** _Default allowed; see banned features below_
*   **C++14:** _Default allowed_
*   **C++17:** _Default allowed; see banned features below_
*   **C++20:** _Initially supported November 13, 2023; see allowed/banned/TBD
    features below_
*   **C++23:** _Not yet supported_
*   **Abseil:** _Default allowed; see banned/TBD features below. The following
    dates represent the start of the two-year TBD periods for certain parts of
    Abseil:_
      * absl::AnyInvocable: Initially added to third_party June 20, 2022
      * Log library: Initially added to third_party Aug 31, 2022
      * CRC32C library: Initially added to third_party Dec 5, 2022
      * Nullability annotation: Initially added to third_party Jun 21, 2023
      * Overload: Initially added to third_party Sep 27, 2023
      * NoDestructor: Initially added to third_party Nov 15, 2023

## Banned features and third-party code

Third-party libraries may generally use banned features internally, although features
with poor compiler support or poor security properties may make the library
unsuitable to use with Chromium.

Chromium code that calls functions exported from a third-party library may use
banned library types that are required by the interface, as long as:

 * The disallowed type is used only at the interface, and converted to and from
   an equivalent allowed type as soon as practical on the Chromium side.
 * The feature is not banned due to security issues or lack of compiler support.
   If it is, discuss with
   [cxx@chromium.org](https://groups.google.com/a/chromium.org/forum/#!forum/cxx)
   to find a workaround.

[TOC]

## C++11 Banned Language Features {#core-blocklist-11}

The following C++11 language features are not allowed in the Chromium codebase.

### Inline Namespaces <sup>[banned]</sup>

```c++
inline namespace foo { ... }
```

**Description:** Allows better versioning of namespaces.

**Documentation:**
[Inline namespaces](https://en.cppreference.com/w/cpp/language/namespace#Inline_namespaces)

**Notes:**
*** promo
Banned in the
[Google Style Guide](https://google.github.io/styleguide/cppguide.html#Namespaces).
Unclear how it will work with components.
***

### long long Type <sup>[banned]</sup>

```c++
long long var = value;
```

**Description:** An integer of at least 64 bits.

**Documentation:**
[Fundamental types](https://en.cppreference.com/w/cpp/language/types)

**Notes:**
*** promo
Use a `<stdint.h>` type if you need a 64-bit number.

[Discussion thread](https://groups.google.com/a/chromium.org/forum/#!topic/chromium-dev/RxugZ-pIDxk)
***

### User-Defined Literals <sup>[banned]</sup>

```c++
DistanceType var = 12_km;
```

**Description:** Allows user-defined literal expressions.

**Documentation:**
[User-defined literals](https://en.cppreference.com/w/cpp/language/user_literal)

**Notes:**
*** promo
Banned in the
[Google Style Guide](https://google.github.io/styleguide/cppguide.html#Operator_Overloading).
***

## C++11 Banned Library Features {#library-blocklist-11}

The following C++11 library features are not allowed in the Chromium codebase.

### &lt;cctype&gt;, &lt;ctype.h&gt;, &lt;cwctype&gt;, &lt;wctype.h&gt; <sup>[banned]</sup>

```c++
#include <cctype>
#include <cwctype>
#include <ctype.h>
#include <wctype.h>
```

**Description:** Provides utilities for ASCII characters.

**Documentation:**
[Standard library header `<cctype>`](https://en.cppreference.com/w/cpp/header/cctype),
[Standard library header `<cwctype>`](https://en.cppreference.com/w/cpp/header/cwctype)

**Notes:**
*** promo
Banned due to dependence on the C locale as well as UB when arguments don't fit
in an `unsigned char`/`wchar_t`. Use similarly-named replacements in
[third_party/abseil-cpp/absl/strings/ascii.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/strings/ascii.h)
instead.
***

### &lt;cfenv&gt;, &lt;fenv.h&gt; <sup>[banned]</sup>

```c++
#include <cfenv>
#include <fenv.h>
```

**Description:** Provides floating point status flags and control modes for
C-compatible code.

**Documentation:**
[Standard library header `<cfenv>`](https://en.cppreference.com/w/cpp/header/cfenv)

**Notes:**
*** promo
Banned by the
[Google Style Guide](https://google.github.io/styleguide/cppguide.html#C++11)
due to concerns about compiler support.
***

### &lt;chrono&gt; <sup>[banned]</sup>

```c++
#include <chrono>
```

**Description:** A standard date and time library.

**Documentation:**
[Date and time utilities](https://en.cppreference.com/w/cpp/chrono)

**Notes:**
*** promo
Overlaps with `base/time`.
***

### &lt;exception&gt; <sup>[banned]</sup>

```c++
#include <exception>
```

**Description:** Exception throwing and handling.

**Documentation:**
[Standard library header `<exception>`](https://en.cppreference.com/w/cpp/header/exception)

**Notes:**
*** promo
Exceptions are banned by the
[Google Style Guide](https://google.github.io/styleguide/cppguide.html#Exceptions)
and disabled in Chromium compiles. However, the `noexcept` specifier is
explicitly allowed.

[Discussion thread](https://groups.google.com/a/chromium.org/forum/#!topic/chromium-dev/8i4tMqNpHhg)
***

### Engines And Generators From &lt;random&gt; <sup>[banned]</sup>

```c++
std::mt19937 generator;
```

**Description:** Methods of generating random numbers.

**Documentation:**
[Pseudo-random number generation](https://en.cppreference.com/w/cpp/numeric/random)

**Notes:**
*** promo
Do not use any random number engines or generators from `<random>`. Instead, use
`base::RandomBitGenerator`. (You may use the distributions from `<random>`.)

[Discussion thread](https://groups.google.com/a/chromium.org/forum/#!topic/cxx/16Xmw05C-Y0)
***

### &lt;ratio&gt; <sup>[banned]</sup>

```c++
#include <ratio>
```

**Description:** Provides compile-time rational numbers.

**Documentation:**
[`std::ratio`](https://en.cppreference.com/w/cpp/numeric/ratio/ratio)

**Notes:**
*** promo
Banned by the
[Google Style Guide](https://google.github.io/styleguide/cppguide.html#C++11)
due to concerns that this is tied to a more template-heavy interface style.
***

### &lt;regex&gt; <sup>[banned]</sup>

```c++
#include <regex>
```

**Description:** A standard regular expressions library.

**Documentation:**
[Regular expressions library](https://en.cppreference.com/w/cpp/regex)

**Notes:**
*** promo
Overlaps with many regular expression libraries in Chromium. When in doubt, use
`third_party/re2`.
***

### std::aligned_{storage,union} <sup>[banned]</sup>

```c++
std::aligned_storage<sizeof(T), alignof<T>>::type buf;
```

**Description:** Creates aligned, uninitialized storage to later hold one or
more objects.

**Documentation:**
[`std::aligned_storage`](https://en.cppreference.com/w/cpp/types/aligned_storage)

**Notes:**
*** promo
Deprecated in C++23. Generally, use `alignas(T) char buf[sizeof(T)];`. Aligned
unions can be handled similarly, using the max alignment and size of the union
members, either passed via a pack or computed inline.
***

### std::bind <sup>[banned]</sup>

```c++
auto x = std::bind(function, args, ...);
```

**Description:** Declares a function object bound to certain arguments.

**Documentation:**
[`std::bind`](https://en.cppreference.com/w/cpp/utility/functional/bind)

**Notes:**
*** promo
Use `base::Bind` instead. Compared to `std::bind`, `base::Bind` helps prevent
lifetime issues by preventing binding of capturing lambdas and by forcing
callers to declare raw pointers as `Unretained`.

[Discussion thread](https://groups.google.com/a/chromium.org/forum/#!topic/cxx/SoEj7oIDNuA)
***

### std::function <sup>[banned]</sup>

```c++
std::function x = [] { return 10; };
std::function y = std::bind(foo, args);
```

**Description:** Wraps a standard polymorphic function.

**Documentation:**
[`std::function`](https://en.cppreference.com/w/cpp/utility/functional/function)

**Notes:**
*** promo
Use `base::{Once,Repeating}Callback` or `base::FunctionRef` instead. Compared
to `std::function`, `base::{Once,Repeating}Callback` directly supports
Chromium's refcounting classes and weak pointers and deals with additional
thread safety concerns.

[Discussion thread](https://groups.google.com/a/chromium.org/forum/#!topic/cxx/SoEj7oIDNuA)
***

### std::shared_ptr <sup>[banned]</sup>

```c++
std::shared_ptr<int> x = std::make_shared<int>(10);
```

**Description:** Allows shared ownership of a pointer through reference counts.

**Documentation:**
[`std::shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr)

**Notes:**
*** promo
Unlike `base::RefCounted`, uses extrinsic rather than intrinsic reference
counting. Could plausibly be used in Chromium, but would require significant
migration.

[Google Style Guide](https://google.github.io/styleguide/cppguide.html#Ownership_and_Smart_Pointers),
[Discussion thread](https://groups.google.com/a/chromium.org/forum/#!topic/cxx/aT2wsBLKvzI)
***

### std::{sto{i,l,ul,ll,ull,f,d,ld},to_string} <sup>[banned]</sup>

```c++
int x = std::stoi("10");
```

**Description:** Converts strings to/from numbers.

**Documentation:**
[`std::stoi`, `std::stol`, `std::stoll`](https://en.cppreference.com/w/cpp/string/basic_string/stol),
[`std::stoul`, `std::stoull`](https://en.cppreference.com/w/cpp/string/basic_string/stoul),
[`std::stof`, `std::stod`, `std::stold`](https://en.cppreference.com/w/cpp/string/basic_string/stof),
[`std::to_string`](https://en.cppreference.com/w/cpp/string/basic_string/to_string)

**Notes:**
*** promo
The string-to-number conversions rely on exceptions to communicate failure,
while the number-to-string conversions have performance concerns and depend on
the locale. Use `base/strings/string_number_conversions.h` instead.
***

### std::weak_ptr <sup>[banned]</sup>

```c++
std::weak_ptr<int> x = my_shared_x;
```

**Description:** Allows a weak reference to a `std::shared_ptr`.

**Documentation:**
[`std::weak_ptr`](https://en.cppreference.com/w/cpp/memory/weak_ptr)

**Notes:**
*** promo
Banned because `std::shared_ptr` is banned.  Use `base::WeakPtr` instead.
***

### Thread Support Library <sup>[banned]</sup>

```c++
#include <barrier>             // C++20
#include <condition_variable>
#include <future>
#include <latch>               // C++20
#include <mutex>
#include <semaphore>           // C++20
#include <stop_token>          // C++20
#include <thread>
```

**Description:** Provides a standard multithreading library using `std::thread`
and associates

**Documentation:**
[Thread support library](https://en.cppreference.com/w/cpp/thread)

**Notes:**
*** promo
Overlaps with `base/synchronization`. `base::Thread` is tightly coupled to
`base::MessageLoop` which would make it hard to replace. We should investigate
using standard mutexes, or `std::unique_lock`, etc. to replace our
locking/synchronization classes.
***

## C++17 Banned Language Features {#core-blocklist-17}

The following C++17 language features are not allowed in the Chromium codebase.

### UTF-8 character literals <sup>[banned]</sup>

```c++
char x = u8'x';     // C++17
char8_t x = u8'x';  // C++20
```

**Description:** A character literal that begins with `u8` is a character
literal of type `char` (C++17) or `char8_t` (C++20). The value of a UTF-8
character literal is equal to its ISO 10646 code point value.

**Documentation:**
[Character literal](https://en.cppreference.com/w/cpp/language/character_literal)

**Notes:**
*** promo
Banned because `char8_t` is banned. Use an unprefixed character or string
literal; it should be encoded in the binary as UTF-8 on all supported platforms.
***

## C++17 Banned Library Features {#library-blocklist-17}

The following C++17 library features are not allowed in the Chromium codebase.

### Mathematical special functions <sup>[banned]</sup>

```c++
std::assoc_laguerre()
std::assoc_legendre()
std::beta()
std::comp_ellint_1()
std::comp_ellint_2()
std::comp_ellint_3()
std::cyl_bessel_i()
std::cyl_bessel_j()
std::cyl_bessel_k()
std::cyl_neumann()
std::ellint_1()
std::ellint_2()
std::ellint_3()
std::expint()
std::hermite()
std::legendre()
std::laguerre()
std::riemann_zeta()
std::sph_bessel()
std::sph_legendre()
std::sph_neumann()
```

**Description:** A variety of mathematical functions.

**Documentation:**
[Mathematical special functions](https://en.cppreference.com/w/cpp/numeric/special_functions)

**Notes:**
*** promo
Banned due to
[lack of libc++ support](https://libcxx.llvm.org/Status/Cxx17.html).
***

### Parallel algorithms <sup>[banned]</sup>

```c++
auto it = std::find(std::execution::par, std::begin(vec), std::end(vec), 2);
```

**Description:** Many of the STL algorithms, such as the `copy`, `find` and
`sort` methods, now support the parallel execution policies: `seq`, `par`, and
`par_unseq` which translate to "sequentially", "parallel" and
"parallel unsequenced".

**Documentation:**
[`std::execution::sequenced_policy`, `std::execution::parallel_policy`, `std::execution::parallel_unsequenced_policy`, `std::execution::unsequenced_policy`](https://en.cppreference.com/w/cpp/algorithm/execution_policy_tag_t)

**Notes:**
*** promo
Banned because
[libc++ support is incomplete](https://libcxx.llvm.org/Status/PSTL.html) and the
interaction of its threading implementation with Chrome's is unclear. Prefer to
explicitly parallelize long-running algorithms using Chrome's threading APIs, so
the same scheduler controls, shutdown policies, tracing, etc. apply as in any
other multithreaded code.
***

### std::aligned_alloc <sup>[banned]</sup>

```c++
int* p2 = static_cast<int*>(std::aligned_alloc(1024, 1024));
```

**Description:** Allocates uninitialized storage with the specified alignment.

**Documentation:**
[`std::aligned_alloc`](https://en.cppreference.com/w/cpp/memory/c/aligned_alloc)

**Notes:**
*** promo
[Will be allowed soon](https://crbug.com/1412818); for now, use
`base::AlignedAlloc`.
***

### std::any <sup>[banned]</sup>

```c++
std::any x = 5;
```

**Description:** A type-safe container for single values of any type.

**Documentation:**
[`std::any`](https://en.cppreference.com/w/cpp/utility/any)

**Notes:**
*** promo
Banned since workaround for lack of RTTI
[isn't compatible with the component build](https://crbug.com/1096380). See also
`absl::any`.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/00cpZ07nye4)
***

### std::byte <sup>[banned]</sup>

```c++
std::byte b = 0xFF;
int i = std::to_integer<int>(b);  // 0xFF
```

**Description:** The contents of a single memory unit. `std::byte` has the same
size and aliasing rules as `unsigned char`, but does not semantically represent
a character or arithmetic value, and does not expose operators other than
bitwise ops.

**Documentation:**
[`std::byte`](https://en.cppreference.com/w/cpp/types/byte)

**Notes:**
*** promo
Banned due to low marginal utility in practice, high conversion costs, and
programmer confusion about "byte" vs. "octet". Use `uint8_t` for the common case
of "8-bit unsigned value", and `char` for the atypical case of code that works
with memory without regard to its contents' values or semantics (e.g allocator
implementations).

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/bBY0gZa1Otk)
***

### std::filesystem <sup>[banned]</sup>

```c++
#include <filesystem>
```

**Description:** A standard way to manipulate files, directories, and paths in a
filesystem.

**Documentation:**
[Filesystem library](https://en.cppreference.com/w/cpp/filesystem)

**Notes:**
*** promo
Banned by the [Google Style Guide](https://google.github.io/styleguide/cppguide.html#Other_Features).
***

### std::{from,to}_chars <sup>[banned]</sup>

```c++
std::from_chars(str.data(), str.data() + str.size(), result);
std::to_chars(str.data(), str.data() + str.size(), 42);
```

**Description:** Locale-independent, non-allocating, non-throwing functions to
convert values from/to character strings, designed for use in high-throughput
contexts.

**Documentation:**
[`std::from_chars`](https://en.cppreference.com/w/cpp/utility/from_chars)
[`std::to_chars`](https://en.cppreference.com/w/cpp/utility/to_chars),

**Notes:**
*** promo
Overlaps with utilities in `base/strings/string_number_conversions.h`, which are
easier to use correctly.
***

### std::in_place{_type,_index}[_t] <sup>[banned]</sup>

```c++
std::variant<int, float> v{std::in_place_type<int>, 1.4};
```

**Description:** `std::in_place_type` and `std::in_place_index` are
disambiguation tags for `std::variant` and `std::any` to indicate that the
object should be constructed in-place.

**Documentation:**
[`std::in_place_type`](https://en.cppreference.com/w/cpp/utility/in_place)

**Notes:**
*** promo
Banned for now because `std::variant` and `std::any` are banned. Because
`absl::variant` is used instead, and it requires `absl::in_place_type`, use
`absl::in_place_type` for non-Abseil Chromium
code.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/ZspmuJPpv6s)
***

### std::{pmr::memory_resource,polymorphic_allocator} <sup>[banned]</sup>

```c++
#include <memory_resource>
```

**Description:** Manages memory allocations using runtime polymorphism.

**Documentation:**
[`std::pmr::memory_resource`](https://en.cppreference.com/w/cpp/memory/memory_resource),
[`std::pmr::polymorphic_allocator`](https://en.cppreference.com/w/cpp/memory/polymorphic_allocator)

**Notes:**
*** promo
Banned because Chromium does not customize allocators
([PartitionAlloc](https://chromium.googlesource.com/chromium/src/+/main/base/allocator/partition_allocator/PartitionAlloc.md)
is used globally).
***

### std::timespec_get <sup>[banned]</sup>

```c++
std::timespec ts;
std::timespec_get(&ts, TIME_UTC);
```

**Description:** Gets the current calendar time in the given time base.

**Documentation:**
[`std::timespec_get`](https://en.cppreference.com/w/cpp/chrono/c/timespec_get)

**Notes:**
*** promo
Banned due to unclear, implementation-defined behavior. On POSIX, use
`base::TimeDelta::ToTimeSpec()`; this could be supported on other platforms if
desirable.
***

### std::uncaught_exceptions <sup>[banned]</sup>

```c++
int count = std::uncaught_exceptions();
```

**Description:** Determines whether there are live exception objects.

**Documentation:**
[`std::uncaught_exceptions`](https://en.cppreference.com/w/cpp/error/uncaught_exception)

**Notes:**
*** promo
Banned because exceptions are banned.
***

### std::variant <sup>[banned]</sup>

```c++
std::variant<int, double> v = 12;
```

**Description:** The class template `std::variant` represents a type-safe
`union`. An instance of `std::variant` at any given time holds a value of one of
its alternative types (it's also possible for it to be valueless).

**Documentation:**
[`std::variant`](https://en.cppreference.com/w/cpp/utility/variant)

**Notes:**
*** promo
[Will be allowed soon](https://crbug.com/1373620); for now, use `absl::variant`.
***

### Transparent std::owner_less <sup>[banned]</sup>

```c++
std::map<std::weak_ptr<T>, U, std::owner_less<>>
```

**Description:** Function object providing mixed-type owner-based ordering of
shared and weak pointers, regardless of the type of the pointee.

**Documentation:**
[`std::owner_less`](https://en.cppreference.com/w/cpp/memory/owner_less)

**Notes:**
*** promo
Banned since `std::shared_ptr` and `std::weak_ptr` are banned.
***

### weak_from_this <sup>[banned]</sup>

```c++
auto weak_ptr = weak_from_this();
```

**Description:** Returns a `std::weak_ptr<T>` that tracks ownership of `*this`
by all existing `std::shared_ptr`s that refer to `*this`.

**Documentation:**
[`std::enable_shared_from_this<T>::weak_from_this`](https://en.cppreference.com/w/cpp/memory/enable_shared_from_this/weak_from_this)

**Notes:**
*** promo
Banned since `std::shared_ptr` and `std::weak_ptr` are banned.
***

## C++20 Allowed Language Features {#core-allowlist-20}

The following C++20 language features are allowed in the Chromium codebase.

### Abbreviated function templates <sup>[allowed]</sup>

```c++
// template <typename T>
// void f1(T x);
void f1(auto x);

// template <C T>  // `C` is a concept
// void f2(T x);
void f2(C auto x);

// template <typename T, C U>  // `C` is a concept
// void f3(T x, U y);
template <typename T>
void f3(T x, C auto y);

// template<typename... Ts>
// void f4(Ts... xs);
void f4(auto... xs);
```

**Description:** Function params of type `auto` become syntactic sugar for
declaring a template type for each such parameter.

**Documentation:**
[Abbreviated function template](https://en.cppreference.com/w/cpp/language/function_template#Abbreviated_function_template)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414526)
***

### consteval <sup>[allowed]</sup>

```c++
consteval int sqr(int n) { return n * n; }
constexpr int kHundred = sqr(10);                  // OK
constexpr int quad(int n) { return sqr(sqr(n)); }  // ERROR, might be runtime
```

**Description:** Specified that a function may only be used in a compile-time
context.

**Documentation:**
[`consteval` specifier](https://en.cppreference.com/w/cpp/language/consteval)

**Notes:**
*** promo
None
***

### Constraints and concepts <sup>[allowed]</sup>

```c++
// `Hashable` is a concept satisfied by any type `T` for which the expression
// `std::hash<T>{}(a)` compiles and produces a value convertible to `size_t`.
template<typename T>
concept Hashable = requires(T a)
{
    { std::hash<T>{}(a) } -> std::convertible_to<size_t>;
};
template <Hashable T>  // Only instantiable for `T`s that satisfy `Hashable`.
void f(T) { ... }
```

**Description:** Allows bundling sets of requirements together as named
concepts, then enforcing them on template arguments.

**Documentation:**
[Constraints and concepts](https://en.cppreference.com/w/cpp/language/constraints)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414528)
***

### Default comparisons <sup>[allowed]</sup>

```c++
class S : public T {
  // Non-member equality operator with access to private members.
  // Compares `T` bases, then `x`, then `y`, short-circuiting when
  // it finds inequality.
  friend bool operator==(const S&, const S&) = default;

  // Non-member ordering operator with access to private members.
  // Compares `T` bases, then `x`, then `y`, short-circuiting when
  // it finds an ordering difference.
  friend auto operator<=>(const S&, const S&) = default;

  int x;
  bool y;
};
```

**Description:** Requests that the compiler generate the implementation of
any comparison operator, including `<=>`. Prefer non-member comparison
operators. When defaulting `<=>`, also explicitly default `==`. Together these
are sufficient to allow any comparison as long as callers do not need to take
the address of any non-declared operator.

**Documentation:**
[Default comparisons](https://en.cppreference.com/w/cpp/language/default_comparisons)

**Notes:**
*** promo
Unlike constructors/destructors, our compiler extensions do not require these
to be written out-of-line in the .cc file. Feel free to write `= default`
directly in the header, as this is much simpler to write.

- [Migration bug](https://crbug.com/1414530)
- [Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/h4lVi2jHU-0/m/X0q_Bh2IAAAJ)

***

### Designated initializers <sup>[allowed]</sup>

```c++
struct S { int x = 1; int y = 2; }
S s{ .y = 3 };  // OK, s.x == 1, s.y == 3
```

**Description:** Allows explicit initialization of subsets of aggregate members
at construction.

**Documentation:**
[Designated initializers](https://en.cppreference.com/w/cpp/language/aggregate_initialization#Designated_initializers)

**Notes:**
*** promo
None
***

### __has_cpp_attribute <sup>[allowed]</sup>

```c++
#if __has_cpp_attribute(assume)  // Toolchain supports C++23 `[[assume]]`.
...
#endif
```

**Description:** Checks whether the toolchain supports a particular standard
attribute.

**Documentation:**
[Feature testing](https://en.cppreference.com/w/cpp/feature_test)

**Notes:**
*** promo
None
***

### constinit <sup>[allowed]</sup>

```c++
constinit int x = 3;
void foo() {
  ++x;
}
```

**Description:** Ensures that a variable can be compile-time initialized. This
is like a milder form of `constexpr` that does not force variables to be const
or have constant destruction.

**Documentation:**
[`constinit` specifier](https://en.cppreference.com/w/cpp/language/constinit)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414612)
***

### Initializers for bit-field members <sup>[allowed]</sup>

```c++
struct S {
  uint32_t x : 27 = 2;
};
```

**Description:** Allows specifying the default initial value of a bit-field
member, as can already be done for other member types.

**Documentation:**
[Bit-field](https://en.cppreference.com/w/cpp/language/bit_field)

**Notes:**
*** promo
None
***

### Lambda captures with initializers that are pack expansions <sup>[allowed]</sup>

```c++
template <typename... Args>
void foo(Args... args) {
  const auto l = [...n = args] { (x(n), ...); };
}
```

**Description:** Allows initializing a capture with a pack expansion.

**Documentation:**
[Lambda capture](https://en.cppreference.com/w/cpp/language/lambda#Lambda_capture)

**Notes:**
*** promo
None
***

### Language feature-test macros <sup>[allowed]</sup>

```c++
#if !defined(__cpp_modules) || (__cpp_modules < 201907L)
...  // Toolchain does not support modules
#endif
```

**Description:** Provides a standardized way to test the toolchain's
implementation of a particular language feature.

**Documentation:**
[Feature testing](https://en.cppreference.com/w/cpp/feature_test)

**Notes:**
*** promo
None
***

### [[likely]], [[unlikely]] <sup>[allowed]</sup>

```c++
if (n > 0) [[likely]] {
  return 1;
}
```

**Description:** Tells the optimizer that a particular codepath is more or less
likely than an alternative.

**Documentation:**
[C++ attribute: `likely`, `unlikely`](https://en.cppreference.com/w/cpp/language/attributes/likely)

**Notes:**
*** promo
[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/bk9YC5qSDF8)
***

### Range-for statements with initializer <sup>[allowed]</sup>

```c++
T foo();
...
for (auto& x : foo().items()) { ... }                   // UAF before C++23!
for (T thing = foo(); auto& x : thing.items()) { ... }  // OK
```

**Description:** Like C++17's selection statements with initializer.
Particularly useful before C++23, since temporaries inside range-expressions are
not lifetime-extended until the end of the loop before C++23.

**Documentation:**
[Range-based `for` loop](https://en.cppreference.com/w/cpp/language/range-for)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414531)
***

### Three-way comparison ("spaceship") operator <sup>[allowed]</sup>

```c++
// `ordering` is an instance of `std::strong_odering` or `std::partial_ordering`
// that describes how `a` and `b` are related.
const auto ordering = a <=> b;
if (ordering < 0) { ... }       // `a` < `b`
else if (ordering > 0) { ... }  // `a` > `b`
else { ... }                    // `a` == `b`
```

**Description:** Compares two objects in a fashion similar to `strcmp`. Perhaps
most useful when defined as an overload in a class, in which case it can replace
definitions of other inequalities. See also "Default comparisons".

**Documentation:**
[Three-way comparison](https://en.cppreference.com/w/cpp/language/operator_comparison#Three-way_comparison)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414530)
***

### using enum declarations <sup>[allowed]</sup>

```c++
enum class E { kA = 1 };
void f() {
  using enum E;
  auto a = kA;
}
```

**Description:** Introduces enumerator element names into the current scope.

**Documentation:**
[`using enum` declaration](https://en.cppreference.com/w/cpp/language/enum#using_enum_declaration)

**Notes:**
*** promo
Usage is subject to the Google Style
[guidelines on aliases](https://google.github.io/styleguide/cppguide.html#Aliases).

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/Y0lf-DSOR3A)
***

## C++20 Allowed Library Features {#library-allowlist-20}

The following C++20 library features are allowed in the Chromium codebase.

### &lt;bit&gt; <sup>[allowed]</sup>

```c++
#include <bit>
```

**Description:** Provides various byte- and bit-twiddling functions, e.g.
counting leading zeros.

**Documentation:**
[Standard library header `<bit>`](https://en.cppreference.com/w/cpp/header/bit)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414634)
***

### &lt;compare&gt; <sup>[allowed]</sup>

```c++
#include <compare>
```

**Description:** Concepts and classes used to implement three-way comparison
("spaceship", `<=>`) support.

**Documentation:**
[Standard library header `<compare>`](https://en.cppreference.com/w/cpp/header/compare)

**Notes:**
*** promo
None
***

### &lt;concepts&gt; <sup>[allowed]</sup>

```c++
#include <concepts>
```

**Description:** Various useful concepts, many of which replace pre-concept
machinery in `<type_traits>`.

**Documentation:**
[Standard library header `<concepts>`](https://en.cppreference.com/w/cpp/header/concepts)

**Notes:**
*** promo
None
***

### Range algorithms <sup>[allowed]</sup>

```c++
constexpr int kArr[] = {2, 4, 6, 8, 10, 12};
constexpr auto is_even = [] (auto x) { return x % 2 == 0; };
static_assert(std::ranges::all_of(kArr, is_even));
```

**Description:** Provides versions of most algorithms that accept either an
iterator-sentinel pair or a single range argument.

**Documentation:**
[Ranges algorithms](https://en.cppreference.com/w/cpp/algorithm/ranges)

**Notes:**
*** promo
Supersedes `//base`'s backports in `//base/ranges/algorithm.h`.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/ZnIbkfJ0Glw)
***

### Range access, range primitives, dangling iterator handling, and range concepts <sup>[allowed]</sup>

```c++
// Range access:
constexpr int kArr[] = {2, 4, 6, 8, 10, 12};
static_assert(std::ranges::size(kArr) == 6);

// Range primitives:
static_assert(
    std::same_as<std::ranges::iterator_t<decltype(kArr)>, const int*>);

// Range concepts:
static_assert(std::ranges::contiguous_range<decltype(kArr)>);
```

**Description:** Various helper functions and types for working with ranges.

**Documentation:**
[Ranges library](https://en.cppreference.com/w/cpp/ranges)

**Notes:**
*** promo
Supersedes `//base`'s backports in `//base//ranges/ranges.h`.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/ZnIbkfJ0Glw)
***

### Library feature-test macros and &lt;version&gt; <sup>[allowed]</sup>

```c++
#if !defined(__cpp_lib_atomic_value_initialization) || \
    (__cpp_lib_atomic_value_initialization < 201911L)
...  // `std::atomic` is not value-initialized by default.
#endif
```

**Description:** Provides a standardized way to test the toolchain's
implementation of a particular library feature.

**Documentation:**
[Feature testing](https://en.cppreference.com/w/cpp/feature_test)

**Notes:**
*** promo
None
***

### &lt;numbers&gt; <sup>[allowed]</sup>

```c++
#include <numbers>
```

**Description:** Provides compile-time constants for many common mathematical
values, e.g. pi and e.

**Documentation:**
[Mathematical constants](https://en.cppreference.com/w/cpp/numeric/constants)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414635)
***

### std::assume_aligned <sup>[allowed]</sup>

```c++
void f(int* p) {
  int* aligned = std::assume_aligned<256>(p);
  ...
```

**Description:** Informs the compiler that a pointer points to an address
aligned to at least some particular power of 2.

**Documentation:**
[`std::assume_aligned`](https://en.cppreference.com/w/cpp/memory/assume_aligned)

**Notes:**
*** promo
None
***

### std::erase[_if] for containers <sup>[allowed]</sup>

```c++
std::vector<int> numbers = ...;
std::erase_if(numbers, [](int x) { return x % 2 == 0; });
```

**Description:** Erases from a container by value comparison or predicate,
avoiding the need to use the `erase(remove(...` paradigm.

**Documentation:**
[`std::erase`, `std::erase_if` (`std::vector`)](https://en.cppreference.com/w/cpp/container/vector/erase2)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414639)
***

### std::hardware_{con,de}structive_interference_size <sup>[allowed]</sup>

```c++
struct SharedData {
  ReadOnlyFrequentlyUsed data;
  alignas(std::hardware_destructive_interference_size) std::atomic<size_t> counter;
};
```

**Description:** The `std::hardware_destructive_interference_size` constant is
useful to avoid false sharing (destructive interference) between variables that
would otherwise occupy the same cacheline. In contrast,
`std::hardware_constructive_interference_size` is helpful to promote true
sharing (constructive interference), e.g. to support better locality for
non-contended data.

**Documentation:**
[`std::hardware_destructive_interference_size`](https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size),
[`std::hardware_constructive_interference_size`](https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size)

**Notes:**
*** promo
[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/cwktrFxxUY4)
***

### std::is_[un]bounded_array <sup>[allowed]</sup>

```c++
template <typename T>
static constexpr bool kBoundedArray = std::is_bounded_array_v<T>;
```

**Description:** Checks if a type is an array type with a known or unknown
bound.

**Documentation:**
[`std::is_bounded_array`](https://en.cppreference.com/w/cpp/types/is_bounded_array),
[`std::is_unbounded_array`](https://en.cppreference.com/w/cpp/types/is_unbounded_array)

**Notes:**
*** promo
None
***

### std::lerp <sup>[allowed]</sup>

```c++
double val = std::lerp(start, end, t);
```

**Description:** Linearly interpolates (or extrapolates) between two values.

**Documentation:**
[`std::lerp`](https://en.cppreference.com/w/cpp/numeric/lerp)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414537)
***

### std::make_obj_using_allocator etc. <sup>[allowed]</sup>

```c++
auto obj = std::make_obj_using_allocator<Obj>(alloc, ...);
```

**Description:** Constructs an object using
[uses-allocator construction](https://en.cppreference.com/w/cpp/memory/uses_allocator).

**Documentation:**
[`std::make_obj_using_allocator`](https://en.cppreference.com/w/cpp/memory/make_obj_using_allocator)

**Notes:**
*** promo
None
***

### std::make_unique_for_overwrite <sup>[allowed]</sup>

```c++
auto ptr = std::make_unique_for_overwrite<int>();  // `*ptr` is uninitialized
```

**Description:** Like calling `std::unique_ptr<T>(new T)` instead of the more
typical `std::unique_ptr<T>(new T(...))`.

**Documentation:**
[`std::make_unique`, `std::make_unique_for_overwrite`](https://en.cppreference.com/w/cpp/memory/unique_ptr/make_unique)

**Notes:**
*** promo
None
***

### std::midpoint <sup>[allowed]</sup>

```c++
int center = std::midpoint(top, bottom);
```

**Description:** Finds the midpoint between its two arguments, avoiding any
possible overflow. For integral inputs, rounds towards the first argument.

**Documentation:**
[`std::midpoint`](https://en.cppreference.com/w/cpp/numeric/midpoint)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414539)
***

### std::ranges::subrange <sup>[allowed]</sup>

```c++
void transform(const std::multimap<int, char>& map, int key) {
  auto [first, last] = map.equal_range(key);
  for (const auto& [_, value] : std::ranges::subrange(first, last)) {
    ...
```

**Description:** Creates a view from an iterator and a sentinel. Useful for
treating non-contiguous storage (e.g. a `std::map`) as a range.

**Documentation:**
[`std::ranges::subrange`](https://en.cppreference.com/w/cpp/ranges/subrange)

**Notes:**
*** promo
Prefer `base::span` if working with explicitly contiguous data, such as in a
`std::vector`. Use `std::ranges::subrange` when data is non-contiguous, or when
it's an implementation detail that the data is contiguous (e.g.
`base::flat_map`).

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/5VeU5GkPUYI)
***

### std::remove_cvref[_t] <sup>[allowed]</sup>

```c++
template <typename T,
          typename = std::enable_if_t<std::is_same_v<std::remove_cvref_t<T>,
                                                     int>>>
void foo(T t);
```

**Description:** Provides a way to remove const, volatile, and reference
qualifiers from a type.

**Documentation:**
[`std::remove_cvref`](https://en.cppreference.com/w/cpp/types/remove_cvref)

**Notes:**
*** promo
None
***

### std::ssize <sup>[allowed]</sup>

```c++
str.replace(it, it + std::ssize(substr), 1, 'x');
```

**Description:** Returns the size of an object as a signed type.

**Documentation:**
[`std::size`, `std::ssize`](https://en.cppreference.com/w/cpp/iterator/size)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414543)
***

### std::string::(starts,ends)_with <sup>[allowed]</sup>

```c++
const std::string str = "Foo bar";
const bool is_true = str.ends_with("bar");
```

**Description:** Tests whether a string starts or ends with a particular
character or string.

**Documentation:**
[`std::basic_string<CharT,Traits,Allocator>::starts_with`](https://en.cppreference.com/w/cpp/string/basic_string/starts_with),
[`std::basic_string<CharT,Traits,Allocator>::ends_with`](https://en.cppreference.com/w/cpp/string/basic_string/ends_with)

**Notes:**
*** promo
[Migration bug](https://crbug.com/1414647)
***

## C++20 Banned Language Features {#core-blocklist-20}

The following C++20 language features are not allowed in the Chromium codebase.

### char8_t <sup>[banned]</sup>

```c++
char8_t c = u8'x';
```

**Description:** A single UTF-8 code unit. Similar to `unsigned char`, but
considered a distinct type.

**Documentation:**
[Fundamental types](https://en.cppreference.com/w/cpp/language/types#char8_t)

**Notes:**
*** promo
Use `char` and unprefixed character literals. Non-UTF-8 encodings are rare
enough in Chromium that the value of distinguishing them at the type level is
low, and `char8_t*` is not interconvertible with `char*` (what ~all Chromium,
STL, and platform-specific APIs use), so using `u8` prefixes would obligate us
to insert casts everywhere. If you want to declare at a type level that a block
of data is string-like and not an arbitrary binary blob, prefer
`std::string[_view]` over `char*`.
***

### Modules <sup>[banned]</sup>

```c++
export module helloworld; // module declaration

import <iostream>;        // import declaration

export void hello() {     // export declaration
  std::cout << "Hello world!\n";
}
```

**Description:** Modules provide an alternative to many uses of headers which
allows for faster compilation, better tooling support, and reduction of problems
like "include what you use".

**Documentation:**
[Modules](https://en.cppreference.com/w/cpp/language/modules)

**Notes:**
*** promo
Not yet sufficiently supported in Clang and GN. Re-evaluate when support
improves.
***

### [[no_unique_address]] <sup>[banned]</sup>

```c++
struct Empty {};
struct X {
  int i;
  [[no_unique_address]] Empty e;
};
```

**Description:** Allows a data member to be overlapped with other members.

**Documentation:**
[C++ attribute: `no_unique_address`](https://en.cppreference.com/w/cpp/language/attributes/no_unique_address)

**Notes:**
*** promo
Has no effect on Windows, for compatibility with Microsoft's ABI. Use
`NO_UNIQUE_ADDRESS` from `base/compiler_specific.h` instead. Do not use (either
form) on members of unions due to
[potential memory safety problems](https://github.com/llvm/llvm-project/issues/60711).
***

## C++20 Banned Library Features {#library-blocklist-20}

The following C++20 library features are not allowed in the Chromium codebase.

### std::atomic_ref <sup>[banned]</sup>

```c++
struct S { int a; int b; };
S not_atomic;
std::atomic_ref<S> is_atomic(not_atomic);
```

**Description:** Allows atomic access to objects that might not themselves be
atomic types. While any atomic_ref to an object exists, the object must be
accessed exclusively through atomic_ref instances.

**Documentation:**
[`std::atomic_ref`](https://en.cppreference.com/w/cpp/atomic/atomic_ref)

**Notes:**
*** promo
Banned due to being [unimplemented in libc++](https://reviews.llvm.org/D72240).

[Migration bug](https://crbug.com/1422701) (once this is allowed)
***

### std::bind_front <sup>[banned]</sup>

```c++
int minus(int a, int b);
auto fifty_minus_x = std::bind_front(minus, 50);
int forty = fifty_minus_x(10);
```

**Description:** An updated version of `std::bind` with fewer gotchas, similar
to `absl::bind_front`.

**Documentation:**
[`std::bind_front`, `std::bind_back`](https://en.cppreference.com/w/cpp/utility/functional/bind_front)

**Notes:**
*** promo
Overlaps with `base::Bind`.
***

### std::bit_cast <sup>[banned]</sup>

```c++
float quake_rsqrt(float number) {
  long i = std::bit_cast<long>(number);
  i = 0x5f3759df - (i >> 1);  // wtf?
  float y = std::bit_cast<float>(i);
  return y * (1.5f - (0.5f * number * y * y));
}
```

**Description:** Returns an value constructed with the same bits as an value of
a different type.

**Documentation:**
[`std::bit_cast`](https://en.cppreference.com/w/cpp/numeric/bit_cast)

**Notes:**
*** promo
The `std::` version of `bit_cast` allows casting of pointer and reference types,
which is both useless in that it doesn't avoid UB, and dangerous in that it
allows arbitrary casting away of modifiers like `const`. Instead of using
`bit_cast` on pointers, use standard C++ casts. For use on values, use
`base::bit_cast` which does not allow this unwanted usage.
***

### std::{c8rtomb,mbrtoc8} <sup>[banned]</sup>

```c++
std::u8string_view strv = u8"zß水🍌";
std::mbstate_t state;
char out[MB_LEN_MAX] = {0};
for (char8_t c : strv) {
  size_t rc = std::c8rtomb(out, c, &state);
  ...
```

**Description:** Converts a code point between UTF-8 and a multibyte character
encoded using the current C locale.

**Documentation:**
[`std::c8rtomb`](https://en.cppreference.com/w/cpp/string/multibyte/c8rtomb),
[`std::mbrtoc8`](https://en.cppreference.com/w/cpp/string/multibyte/mbrtoc8)

**Notes:**
*** promo
Chromium functionality should not vary with the C locale.
***

### Range factories and range adaptors <sup>[banned]</sup>

```c++
// Prints 1, 2, 3, 4, 5, 6.
for (auto i : std::ranges::iota_view(1, 7)) {
  std::cout << i << '\n';
}

constexpr int kArr[] = {6, 2, 8, 4, 4, 2};
constexpr auto plus_one = std::views::transform([](int n){ return n + 1; });
static_assert(std::ranges::equal(kArr | plus_one, {7, 3, 9, 5, 5, 3}));
```

**Description:** Lightweight objects that represent iterable sequences.
Provides facilities for lazy operations on ranges, along with composition into
pipelines.

**Documentation:**
[Ranges library](https://en.cppreference.com/w/cpp/ranges)

**Notes:**
*** promo
Banned in Chrome due to questions about the design, impact on build time, and
runtime performance.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/ZnIbkfJ0Glw)
***

### std::ranges::view_interface <sup>[banned]</sup>

```c++
class MyView : public std::ranges::view_interface<MyView> { ... };
```

**Description:** CRTP base class for implementing custom view objects.

**Documentation:**
[`std::ranges::view_interface`](https://en.cppreference.com/w/cpp/ranges/view_interface)

**Notes:**
*** promo
Banned in Chrome since range factories and adapters are banned, and this would
primarily allow authors to create similar functionality.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/ZnIbkfJ0Glw)
***

### &lt;span&gt; <sup>[banned]</sup>

```c++
#include <span>
```

**Description:** Utilities for non-owning views over a sequence of objects.

**Documentation:**
[](https://en.cppreference.com/w/cpp/header/span)

**Notes:**
*** promo
Superseded by `base::span`, which has a richer functionality set.
***

### std::to_address <sup>[banned]</sup>

```c++
std::vector<int> numbers;
int* i = std::to_address(numbers.begin());
```

**Description:** Converts a pointer-like object to a pointer, even if the
pointer does not refer to a constructed object (in which case an expression like
`&*p` is UB).

**Documentation:**
[`std::to_address`](https://en.cppreference.com/w/cpp/memory/to_address)

**Notes:**
*** promo
Banned because it is not guaranteed to be SFINAE-compatible. Use
base::to_address, which does guarantee this.
***

### &lt;syncstream&gt; <sup>[banned]</sup>

```c++
#include <syncstream>
```

**Description:** Facilities for multithreaded access to streams.

**Documentation:**
[Standard library header `<syncstream>`](https://en.cppreference.com/w/cpp/header/syncstream)

**Notes:**
*** promo
Banned due to being unimplemented per
[the libc++ C++20 status page](https://libcxx.llvm.org/Status/Cxx20.html).
Reevaluate usefulness once implemented.
***

## C++20 TBD Language Features {#core-review-20}

The following C++20 language features are not allowed in the Chromium codebase.
See the top of this page on how to propose moving a feature from this list into
the allowed or banned sections.

### Aggregate initialization using parentheses <sup>[tbd]</sup>

```c++
struct B {
  int a;
  int&& r;
} b2(1, 1);  // Warning: dangling reference
```

**Description:** Allows initialization of aggregates using parentheses, not just
braces.

**Documentation:**
[Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization),
[Direct initialization](https://en.cppreference.com/w/cpp/language/direct_initialization)

**Notes:**
*** promo
There are subtle but important differences between brace- and paren-init of
aggregates. The parenthesis style appears to have more pitfalls (allowing
narrowing conversions, not extending lifetimes of temporaries bound to
references).
***

### Coroutines <sup>[tbd]</sup>

```c++
co_return 1;
```

**Description:** Allows writing functions that logically block while physically
returning control to a caller. This enables writing some kinds of async code in
simple, straight-line ways without storing state in members or binding
callbacks.

**Documentation:**
[Coroutines](https://en.cppreference.com/w/cpp/language/coroutines)

**Notes:**
*** promo
Requires significant support code and planning around API and migration.

[Prototyping bug](https://crbug.com/1403840)
***

## C++20 TBD Library Features {#library-review-20}

The following C++20 library features are not allowed in the Chromium codebase.
See the top of this page on how to propose moving a feature from this list into
the allowed or banned sections.

### &lt;coroutine&gt; <sup>[tbd]</sup>

```c++
#include <coroutine>
```

**Description:** Header which defines various core coroutine types.

**Documentation:**
[Coroutine support](https://en.cppreference.com/w/cpp/coroutine)

**Notes:**
*** promo
See notes on "Coroutines" above.
***

### &lt;format&gt; <sup>[tbd]</sup>

```c++
std::cout << std::format("Hello {}!\n", "world");
```

**Description:** Utilities for producing formatted strings.

**Documentation:**
[Formatting library](https://en.cppreference.com/w/cpp/utility/format)

**Notes:**
*** promo
Has both pros and cons compared to `absl::StrFormat` (which we don't yet use).
Migration would be nontrivial.
***

### &lt;source_location&gt; <sup>[tbd]</sup>

```c++
#include <source_location>
```

**Description:** Provides a class that can hold source code details such as
filenames, function names, and line numbers.

**Documentation:**
[Standard library header `<source_location>`](https://en.cppreference.com/w/cpp/header/source_location)

**Notes:**
*** promo
Seems to regress code size vs. `base::Location`.
***

### std::u8string <sup>[tbd]</sup>

```c++
std::u8string str = u8"Foo";
```

**Description:** A string whose character type is `char8_t`, intended to hold
UTF-8-encoded text.

**Documentation:**
[`std::basic_string`](https://en.cppreference.com/w/cpp/string/basic_string)

**Notes:**
*** promo
See notes on `char8_t` above.
***

## Abseil Banned Library Features {#absl-blocklist}

The following Abseil library features are not allowed in the Chromium codebase.

### Any <sup>[banned]</sup>

```c++
absl::any a = int{5};
EXPECT_THAT(absl::any_cast<int>(&a), Pointee(5));
EXPECT_EQ(absl::any_cast<size_t>(&a), nullptr);
```

**Description:** Early adaptation of C++17 `std::any`.

**Documentation:** [std::any](https://en.cppreference.com/w/cpp/utility/any)

**Notes:**
*** promo
Banned since workaround for lack of RTTI
[isn't compatible with the component build](https://crbug.com/1096380). See also
`std::any`.
***

### Attributes <sup>[banned]</sup>

```c++
T* data() ABSL_ATTRIBUTE_LIFETIME_BOUND { return data_; }
ABSL_ATTRIBUTE_NO_TAIL_CALL ReturnType Loop();
struct S { bool b; int32_t i; } ABSL_ATTRIBUTE_PACKED;
```

**Description:** Cross-platform macros to expose compiler-specific
functionality.

**Documentation:** [attributes.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/base/attributes.h)

**Notes:**
*** promo
Long names discourage use. Use standardized attributes over macros where
possible, and otherwise prefer shorter alternatives in
`base/compiler_specific.h`.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/lVQOJTng1RU)
***

### btree_\* containers <sup>[banned]</sup>

```c++
absl::btree_map
absl::btree_set
absl::btree_multimap
absl::btree_multiset
```

**Description:** Alternatives to the tree-based standard library containers
designed to be more efficient in the general case.

**Documentation:** [Containers](https://abseil.io/docs/cpp/guides/container)

**Notes:**
*** promo
In theory these should be superior alternatives that could replace most uses of
`std::map` and company. In practice they have been found to introduce a
substantial code size increase. Until this problem can be resolved the use of
these containers is banned. Use the standard library containers instead.
***

### bind_front <sup>[banned]</sup>

```c++
absl::bind_front
```

**Description:** Binds the first N arguments of an invocable object and stores
them by value.

**Documentation:**
*   [bind_front.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/functional/bind_front.h)
*   [Avoid std::bind](https://abseil.io/tips/108)

**Notes:**
*** promo
Overlaps with `base::Bind`.
***

### Command line flags <sup>[banned]</sup>

```c++
ABSL_FLAG(bool, logs, false, "print logs to stderr");
app --logs=true;
```

**Description:** Allows programmatic access to flag values passed on the
command-line to binaries.

**Documentation:** [Flags Library](https://abseil.io/docs/cpp/guides/flags)

**Notes:**
*** promo
Banned since workaround for lack of RTTI
[isn't compatible with the component build](https://crbug.com/1096380). Use
`base::CommandLine` instead.
***

### Container utilities <sup>[banned]</sup>

```c++
auto it = absl::c_find(container, value);
```

**Description:** Container-based versions of algorithmic functions within C++
standard library.

**Documentation:**
[container.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/algorithm/container.h)

**Notes:**
*** promo
Overlaps with `base/ranges/algorithm.h`.
***

### FixedArray <sup>[banned]</sup>

```c++
absl::FixedArray<MyObj> objs_;
```

**Description:** A fixed size array like `std::array`, but with size determined
at runtime instead of compile time.

**Documentation:**
[fixed_array.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/container/fixed_array.h)

**Notes:**
*** promo
Direct construction is banned due to the risk of UB with uninitialized
trivially-default-constructible types. Instead use `base/types/fixed_array.h`,
which is a light-weight wrapper that deletes the problematic constructor.
***

### FunctionRef <sup>[banned]</sup>

```c++
absl::FunctionRef
```

**Description:** Type for holding a non-owning reference to an object of any
invocable type.

**Documentation:**
[function_ref.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/functional/function_ref.h)

**Notes:**
*** promo
- `absl::FunctionRef` is banned due to allowing implicit conversions between
  function signatures in potentially surprising ways. For example, a callable
  with the signature `int()` will bind to `absl::FunctionRef<void()>`: the
  return value from the callable will be silently discarded.
- In Chromium, use `base::FunctionRef` instead.
- Unlike `base::OnceCallback` and `base::RepeatingCallback`, `base::FunctionRef`
  supports capturing lambdas.
- Useful when passing an invocable object to a function that synchronously calls
  the invocable object, e.g. `ForEachFrame(base::FunctionRef<void(Frame&)>)`.
  This can often result in clearer code than code that is templated to accept
  lambdas, e.g. with `template <typename Invocable> void
  ForEachFrame(Invocable invocable)`, it is much less obvious what arguments
  will be passed to `invocable`.
- For now, `base::OnceCallback` and `base::RepeatingCallback` intentionally
  disallow conversions to `base::FunctionRef`, under the theory that the
  callback should be a capturing lambda instead. Attempting to use this
  conversion will trigger a `static_assert` requesting additional feedback for
  use cases where this conversion would be valuable.
- *Important:* `base::FunctionRef` must not outlive the function call. Like
  `std::string_view`, `base::FunctionRef` is a *non-owning* reference. Using a
  `base::FunctionRef` as a return value or class field is dangerous and likely
  to result in lifetime bugs.

[Discussion thread](https://groups.google.com/a/chromium.org/g/cxx/c/JVN4E4IIYA0)
***

### Optional <sup>[banned]</sup>

```c++
absl::optional<int> Func(bool b) {
  return b ? absl::make_optional(1) : abl::nullopt;
}
```

**Description:** Early adaptation of C++17 `std::optional`.

**Documentation:** [std::optional](https://en.cppreference.com/w/cpp/utility/optional)

**Notes:**
*** promo
Superseded by `std::optional`. Use `std::optional` instead.
***

### Random <sup>[banned]</sup>

```c++
absl::BitGen bitgen;
size_t index = absl::Uniform(bitgen, 0u, elems.size());
```

**Description:** Functions and utilities for generating pseudorandom data.

**Documentation:** [Random library](https://abseil.io/docs/cpp/guides/random)

**Notes:**
*** promo
Banned because most uses of random values in Chromium should be using a
cryptographically secure generator. Use `base/rand_util.h` instead.
***

### Span <sup>[banned]</sup>

```c++
absl::Span
```

**Description:** Early adaptation of C++20 `std::span`.

**Documentation:** [Using absl::Span](https://abseil.io/tips/93)

**Notes:**
*** promo
Banned due to being less std::-compliant than `base::span`. Keep using
`base::span`.
***

### StatusOr <sup>[banned]</sup>

```c++
absl::StatusOr<T>
```

**Description:** An object that is either a usable value, or an error Status
explaining why such a value is not present.

**Documentation:**
[statusor.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/status/statusor.h)

**Notes:**
*** promo
Overlaps with `base::expected`.
***

### string_view <sup>[banned]</sup>

```c++
absl::string_view
```

**Description:** Early adaptation of C++17 `std::string_view`.

**Documentation:** [absl::string_view](https://abseil.io/tips/1)

**Notes:**
*** promo
Originally banned due to only working with 8-bit characters. Now it is
unnecessary because, in Chromium, it is the same type as `std::string_view`.
Please use `std::string_view` instead.
***

### Strings Library <sup>[banned]</sup>

```c++
absl::StrSplit
absl::StrJoin
absl::StrCat
absl::StrAppend
absl::Substitute
absl::StrContains
```

**Description:** Classes and utility functions for manipulating and comparing
strings.

**Documentation:**
[String Utilities](https://abseil.io/docs/cpp/guides/strings)

**Notes:**
*** promo
Overlaps with `base/strings`. We
[should re-evalute](https://bugs.chromium.org/p/chromium/issues/detail?id=1371966)
when we've
[migrated](https://bugs.chromium.org/p/chromium/issues/detail?id=691162) from
`base::StringPiece` to `std::string_view`. Also note that `absl::StrFormat()` is
not considered part of this group, and is explicitly allowed.
***

### Synchronization <sup>[banned]</sup>

```c++
absl::Mutex
```

**Description:** Primitives for managing tasks across different threads.

**Documentation:**
[Synchronization](https://abseil.io/docs/cpp/guides/synchronization)

**Notes:**
*** promo
Overlaps with `base/synchronization/`. We would love
[more testing](https://bugs.chromium.org/p/chromium/issues/detail?id=1371969) on
whether there are compelling reasons to prefer base, absl, or std
synchronization primitives; for now, use `base/synchronization/`.
***

### Time library <sup>[banned]</sup>

```c++
absl::Duration
absl::Time
absl::TimeZone
absl::CivilDay
```

**Description:** Abstractions for holding time values, both in terms of
absolute time and civil time.

**Documentation:** [Time](https://abseil.io/docs/cpp/guides/time)

**Notes:**
*** promo
Overlaps with `base/time/`.
***

## Abseil TBD Features {#absl-review}

The following Abseil library features are not allowed in the Chromium codebase.
See the top of this page on how to propose moving a feature from this list into
the allowed or banned sections.

### AnyInvocable <sup>[tbd]</sup>

```c++
absl::AnyInvocable
```

**Description:** An equivalent of the C++23 std::move_only_function.

**Documentation:**
*   [any_invocable.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/functional/any_invocable.h)
*   [std::move_only_function](https://en.cppreference.com/w/cpp/utility/functional/move_only_function/move_only_function)

**Notes:**
*** promo
Overlaps with `base::RepeatingCallback`, `base::OnceCallback`.
***

### CRC32C library <sup>[tbd]</sup>

**Description:** API for computing CRC32C values as checksums for arbitrary
sequences of bytes provided as a string buffer.

**Documentation:**
[crc32.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/crc/crc32c.h)

**Notes:**
*** promo
Overlaps with `third_party/crc32c`.
***

### Log macros and related classes <sup>[tbd]</sup>

```c++
LOG(INFO) << message;
CHECK(condition);
absl::AddLogSink(&custom_sink_to_capture_absl_logs);
```

**Description:** Macros and related classes to perform debug loggings

**Documentation:**
[log.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/log/log.h)
[check.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/log/check.h)

**Notes:**
*** promo
Overlaps with `base/logging.h`.
***

### NoDestructor <sup>[tbd]</sup>

```c++
// Global or namespace scope.
ABSL_CONST_INIT absl::NoDestructor<MyRegistry> reg{"foo", "bar", 8008};

// Function scope.
const std::string& MyString() {
  static const absl::NoDestructor<std::string> x("foo");
  return *x;
}
```

**Description:** `absl::NoDestructor<T>` is a wrapper around an object of
type T that behaves as an object of type T but never calls T's destructor.

**Documentation:**
[no_destructor.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/base/no_desctructor.h)

**Notes:**
*** promo
Overlaps with `base::NoDestructor`.
***

### Nullability annotations <sup>[tbd]</sup>

```c++
void PaySalary(absl::NotNull<Employee *> employee) {
  pay(*employee);  // OK to dereference
}
```

**Description:** Annotations to more clearly specify contracts

**Documentation:**
[nullability.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/base/nullability.h)

**Notes:**
*** promo
These nullability annotations are primarily a human readable signal about the
intended contract of the pointer. They are not *types* and do not currently
provide any correctness guarantees.
***

### Overload <sup>[tbd]</sup>

```c++
std::variant<int, std::string, double> v(int{1});
assert(std::visit(absl::Overload(
                       [](int) -> absl::string_view { return "int"; },
                       [](const std::string&) -> absl::string_view {
                         return "string";
                       },
                       [](double) -> absl::string_view { return "double"; }),
                    v) == "int");
```

**Description:** Returns a functor that provides overloads based on the functors passed to it

**Documentation:**
[overload.h](https://source.chromium.org/chromium/chromium/src/+/main:third_party/abseil-cpp/absl/functional/overload.h)

**Notes:**
*** promo
Overlaps with `base::Overloaded`.
***
