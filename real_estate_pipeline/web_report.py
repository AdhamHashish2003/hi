import pandas as pd

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Dubai Real Estate Opportunities</title>
    <style>
        table {border-collapse: collapse; width: 100%;}
        th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}
        th {background-color: #f2f2f2;}
        img {max-width: 120px; height: auto;}
    </style>
</head>
<body>
    <h1>Dubai Real Estate Opportunities</h1>
    <table>
        <thead>
            <tr>
                <th>Image</th>
                <th>Location</th>
                <th>Price (AED)</th>
                <th>Bedrooms</th>
                <th>Bathrooms</th>
                <th>Sqft</th>
                <th>Furnishing</th>
                <th>Listing Type</th>
                <th>Rental Price</th>
                <th>Gross Yield %</th>
                <th>ROI %</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>
"""


def df_to_rows(df: pd.DataFrame) -> str:
    rows = []
    for _, r in df.iterrows():
        rows.append(
            f"<tr>"
            f"<td><img src='{r.get('image_url', '')}' alt='Image'></td>"
            f"<td><a href='{r.get('url', '#')}' target='_blank'>{r['location']}</a></td>"
            f"<td>{r['price']}</td>"
            f"<td>{r.get('bedrooms','')}</td>"
            f"<td>{r.get('bathrooms','')}</td>"
            f"<td>{r.get('sqft','')}</td>"
            f"<td>{r.get('furnishing','')}</td>"
            f"<td>{r.get('listing_type','')}</td>"
            f"<td>{r.get('rental_price','')}</td>"
            f"<td>{round(r.get('gross_yield',0),2)}</td>"
            f"<td>{round(r.get('estimated_roi',0),2)}</td>"
            f"</tr>"
        )
    return "\n".join(rows)


def generate_html(df: pd.DataFrame, out_path: str = "index.html") -> str:
    rows = df_to_rows(df)
    html = HTML_TEMPLATE.format(rows=rows)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path
