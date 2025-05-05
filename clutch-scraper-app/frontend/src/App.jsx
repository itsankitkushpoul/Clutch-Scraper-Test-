import React, { useState } from 'react';
import { scrape } from './api';

function App() {
  const [url, setUrl] = useState('');
  const [pages, setPages] = useState(3);
  const [data, setData] = useState([]);

  const handleScrape = async () => {
    const res = await scrape(url, pages);
    setData(res.data.results);
  };

  return (
    <div className="p-4">
      <input value={url} onChange={e => setUrl(e.target.value)} placeholder="Clutch URL" />
      <input type="number" value={pages} onChange={e => setPages(e.target.value)} />
      <button onClick={handleScrape}>Scrape</button>
      <table className="mt-4">
        <thead><tr><th>#</th><th>Company</th><th>Website</th><th>Location</th></tr></thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              <td>{i + 1}</td>
              <td>{row['Company Name']}</td>
              <td>{row.Website}</td>
              <td>{row.Location}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
