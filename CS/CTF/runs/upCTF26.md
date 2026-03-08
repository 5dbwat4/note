## [Misc] Jailed (AI solveable)

题面：

```python
import os
API_KEY = os.getenv("FLAG")

class cdm22b:
    def __init__(self):
        self.SAFE_GLOBALS = locals()
        self.SAFE_GLOBALS['__builtins__'] = {}
        self.name = "cdm"
        self.role = "global hacker, hacks planets"
        self.friend = "No one"

    def validateInput(self, input: str) -> tuple[bool, str]:
        if len(input) > 66:
            return False, 'to long, find a shorter way'

        for builtin in dir(__builtins__):
            if builtin.lower() in input.lower():
                return False, 'builtins would be too easy!'

        if any(i in input for i in '\",;`'):
            return False, 'bad bad bad chars!'

        return True, ''


    def safeEval(self, s):
        try:
            eval(s, self.SAFE_GLOBALS)
        except Exception:
            print("Something went wrong")


    def myFriend(self):
        friend = self.SAFE_GLOBALS.get('friend', self.friend)
        print(friend.format(self=self))


if __name__ == '__main__':
    hacker = cdm22b()
    input = input()
    ok, err = hacker.validateInput(input)
    if ok:
        hacker.safeEval(input)
        hacker.myFriend()
    else:
        print(err)
```

`upCTF{fmt_str1ng5_4r3nt_0nly_a_C_th1ng-KReOjU4F194b31d9}`


Prompt: 

> A PyJail CTF Challenge. Tell me how to solve it. Use Code execution tools to verify your thoughts

Response:

To solve this PyJail challenge, we need to inject a specific format string into the `friend` variable. The `myFriend` method executes `print(friend.format(self=self))`, which allows us to access attributes of `self` and leak global variables (like `API_KEY` where the flag is stored) using Python's format string vulnerabilities.

### Restrictions Analysis
1.  **Length Limit:** Payload must be $\le$ 66 characters.
2.  **Builtin Filter:** Cannot use names of builtins (e.g., `globals`, `__import__`, `getattr`) in the input string.
3.  **Character Filter:** Cannot use double quotes (`"`), semicolons (`;`), commas (`,`), or backticks (`` ` ``).
4.  **Sandbox:** `eval` runs with an empty `__builtins__`, preventing standard function calls.

### Attack Vector
1.  **Injection Point:** The `safeEval` function executes `eval(input, SAFE_GLOBALS)`. We can use the **Walrus operator** `:=` (Python 3.8+) to assign a value to `friend` within the `SAFE_GLOBALS` dictionary (since `locals()` was captured into it).
    *   *Payload structure:* `(friend:='...')`
2.  **Format String Exploit:** We want `friend` to be `{self.__init__.__globals__[API_KEY]}`. When `myFriend` calls `.format(self=self)`, this retrieves the `API_KEY` from the module's global scope.
3.  **Bypassing Filters:**
    *   **Quotes:** We can use single quotes `'` to wrap strings.
    *   **"globals" Filter:** The word `globals` is a builtin and blocked. We bypass this by constructing the string using concatenation: `'glo'+'bals'`.
    *   **"__init__" Filter:** Just in case `__init__` is flagged (it sometimes appears in restricted lists), we can split it too: `'__i'+'nit__'`.
    *   **API_KEY Access:** In format strings, `dict[Key]` works without quotes around the key if it's a valid identifier string. So `[API_KEY]` works.

### The Solution Payload
We construct the string `{self.__init__.__globals__[API_KEY]}` dynamically inside the `eval`.

```python
(friend:='{self.__i'+'nit__.__glo'+'bals__[API_KEY]}')
```

**Breakdown:**
*   `(friend:= ... )`: Assigns the result to `friend` inside the restricted globals.
*   `'{self.__i'` + `'nit__.__glo'` + `'bals__[API_KEY]}'` : Concatenates to form the string `"{self.__init__.__globals__[API_KEY]}"`.
*   The input does not contain the substring "globals" or "init", bypassing the builtin check.
*   The length is 54 characters, which is under the limit of 66.
*   It uses only allowed characters (no `"`, `,`, `;`, `` ` ``).

### Final Output

```python
(friend:='{self.__i'+'nit__.__glo'+'bals__[API_KEY]}')
```