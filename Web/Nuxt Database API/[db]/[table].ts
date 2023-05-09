// eslint-disable-next-line import/default
import sql from "mssql";

export default defineEventHandler(async (event) => {
    const query = getQuery(event); // query parameters
    /* useRuntimeConfig().db = {
            server: process.env.DB_SERVER,
            user: process.env.DB_USER,
            password: process.env.DB_PASSWORD,
        }*/
    const db = { ...useRuntimeConfig().db, database: event.context.params?.db }; // [db]
    const table = event.context.params?.table; // [table]

    /* eslint-disable import/no-named-as-default-member */
    await sql.connect(db);
    let result;
    switch (event.node.req.method) {
        case "GET": {
            const startId = query.startId || `(SELECT MIN(id) FROM ${table})`;
            const endId = query.endId || `(SELECT MAX(id) FROM ${table})`;
            let cols: string[] = (query.cols as string[]) || [];
            if (typeof cols === "string") cols = [cols];

            let selectcols: string[] | string = [];
            for (const i in cols) selectcols.push("[" + cols[i] + "]");
            if (selectcols.length > 0) selectcols = selectcols.join(",");
            else selectcols = "*";

            result = await sql.query(
                `SELECT ${selectcols} FROM ${table} WHERE id>=${startId} AND id<=${endId}`
            );
            return result.recordset;
        }

        case "POST": {
            const body = await readBody(event);
            let cols = "";
            let values = "";
            for (const col in body) {
                cols += "[" + col + "],";
                const value = body[col];
                if (typeof value === "string") values += `'${value}',`;
                else values += value + ",";
            }
            cols = cols.slice(0, -1);
            values = values.slice(0, -1);
            result = await sql.query(
                `INSERT INTO ${table}(${cols}) VALUES(${values})`
            );
            return { rowsAffected: result.rowsAffected };
        }

        case "PUT": {
            const body = await readBody(event);
            const updateSet = [];
            for (const col in body) {
                const value = body[col];
                let t = "[" + col + "]=";
                if (typeof value === "string") t += `'${value}'`;
                else t += value;
                updateSet.push(t);
            }
            const updateText = updateSet.join(",");

            const checkcol = Object.keys(body)[0];
            const value =
                typeof body[checkcol] === "string"
                    ? `'${body[checkcol]}'`
                    : body[checkcol];

            result = await sql.query(
                `UPDATE ${table} SET ${updateText} WHERE [${checkcol}]=${value}`
            );
            return { rowsAffected: result.rowsAffected };
        }

        case "DELETE": {
            const body = await readBody(event);
            const col = Object.keys(body)[0];
            const value =
                typeof body[col] === "string" ? `'${body[col]}'` : body[col];
            result = await sql.query(`DELETE FROM ${table} WHERE [${col}]=${value}`);
            return { rowsAffected: result.rowsAffected };
        }
    }
});
