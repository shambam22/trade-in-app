<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Game Trade-In Calculator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light text-dark">
    <div class="container py-5">
        <h1 class="mb-4 text-center">Game Trade-In Calculator</h1>

        <form method="POST" class="mb-4">
            <div class="mb-3">
                <label for="game" class="form-label">Enter Game Title</label>
                <input type="text" id="game" name="game" class="form-control" required placeholder="e.g., The Legend of Zelda">
            </div>

            <button type="submit" class="btn btn-primary">Check Value</button>
        </form>

        {% if trade_data %}
            <div class="card">
                <div class="card-header text-center">
                    <h3 class="card-title">{{ trade_data.title }}</h3>
                </div>
                <div class="card-body">
                    {% if trade_data.image_url %}
                        <div class="text-center mb-4">
                            <img src="{{ trade_data.image_url }}" alt="{{ trade_data.title }}" class="img-fluid" style="max-height: 200px;">
                        </div>
                    {% endif %}
                    <table class="table table-bordered table-striped">
                        <thead class="table-secondary">
                            <tr>
                                <th>Condition</th>
                                <th>Trade-In Credit</th>
                                <th>Cash Offer</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Loose</td>
                                <td>${{ trade_data.loose_credit }}</td>
                                <td>${{ trade_data.loose_cash }}</td>
                            </tr>
                            <tr>
                                <td>Complete (CIB)</td>
                                <td>${{ trade_data.cib_credit }}</td>
                                <td>${{ trade_data.cib_cash }}</td>
                            </tr>
                            <tr>
                                <td>New</td>
                                <td>${{ trade_data.new_credit }}</td>
                                <td>${{ trade_data.new_cash }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        {% elif request.method == 'POST' %}
            <div class="alert alert-warning mt-4">Game not found or API issue. Please check your entry.</div>
        {% endif %}
    </div>
</body>
</html>
