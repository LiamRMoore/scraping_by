import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(title, buyer, keywords, date, link) {
  return { title, buyer, keywords, date, link };
}

const rows = [
  createData('title 1', 'buyer 1', "science, ai, data", '20210730T083000', 'https://demo1.com'),
  createData('title 2', 'buyer 2', 'data', '20210729T223000', 'https://demo2.com'),
];

export default function BasicTable() {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell align="right">Buyer</TableCell>
            <TableCell align="right">Keywords Matched</TableCell>
            <TableCell align="right">Date</TableCell>
            <TableCell align="right">link</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.title}
              </TableCell>
              <TableCell align="right">{row.buyer}</TableCell>
              <TableCell align="right">{row.keywords}</TableCell>
              <TableCell align="right">{row.date}</TableCell>
              <TableCell align="right">{row.link}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
