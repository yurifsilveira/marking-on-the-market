function el(tag, props = {}, children = []) {
    const element = document.createElement(tag);
    Object.assign(element, props);

    children.forEach(child => {
        if (typeof child === "string") {
            element.appendChild(document.createTextNode(child));
        } else {
            element.appendChild(child);
        }
    });

    return element;
}

class Card {
    constructor(data, title) {
        this.data = data;
        this.title = title;
        this.pathImg = "../static/img/public.png"

        this.div = el("div", { 
            className: "col-4 card text-center mt-4" 
        });

        this.div.appendChild(new CardTitle(title, this.pathImg).render());

        const body = new CardBody();

        for (const row of this.data) {
            body.addLine(row, `/rendafixa/detalhes?title=${row.tipo}&deadline=${row.vencimento}`);
        }

        this.div.appendChild(body.render());
    }

    render() {
        return this.div;
    }
}

class CardTitle {
    constructor(title, pathImg) {
        this.div = el("div", {
            className: "card-header d-flex flex-column align-items-center justify-content-center gap-2",
        }, [
            el("img", {"src":pathImg, style: "max-height: 50px;"}),
            el("h5", { className: "fw-semibold", innerText: title })
        ]);
    }

    render() {
        return this.div;
    }
}

class CardBody {
    constructor() {
        this.tbody = el("tbody");
        this.div = el("div", { className: "card-body overflow-y-auto", style: "max-height: 650px;"}, [
            el("table", { className: "table table-hover" }, [
                this.tbody
            ])
        ]);
    }

    addLine(data, router) {

        const imgSrc =  "../static/img/tesouro.svg";

        const tr = el("tr", {
            style: "cursor:pointer;height:90px;vertical-align:middle;display:table-row;",
            onclick: () => window.location = router
        });

        const th = el("th", {}, [
            el("div", { className: "d-flex align-items-center gap-2" }, [
                el("img", { src: imgSrc, alt: "Tesouro Direto", style: "height:35px" }),
                el("h5", { style:"font-size:10px;", innerText: `${data.titulo}` })
            ])
        ]);
        const tdValue = el("td", {
            style: "display:table-cell; align-items:center; font-size:12px;"
        });

        const wrapperValue = el("div", {
            style: "display:flex; flex-direction:column; align-items:center;"
        });

        wrapperValue.append(
            el("span", { innerText: `R$ ${Number(data.pu_compra_manha).toFixed(2)}`, style:"font-size:18px;" }),
            el("label", { innerText: "Preço Atual", style: "font-size:10px; opacity:0.7;" })
        );

        tdValue.append(wrapperValue);

        const tdMedianMovel = el("td", {
            style: "display:table-cell; align-items:center; font-size:12px;"
        });

        const tdMedianMovelWrapper = el("div", {
            style: "display:flex; flex-direction:column; align-items:center;"
        });

        tdMedianMovelWrapper.append(
            el("span", { innerText: `R$ ${Number(data.pu_venda_manha_media_movel).toFixed(2)}`, style:"font-size:18px;" }),
            el("label", { innerText: "Média Movel", style: "font-size:10px; opacity:0.7;" })
        );

        tdMedianMovel.append(tdMedianMovelWrapper);

        const fig = el("td", { className: "fs-5" }, [
            el("img", {
                src: "../static/img/chevron-compact-right.svg",
                alt: "link"
            })
        ]);

        tr.append(th, tdValue,tdMedianMovel, fig);
        this.tbody.appendChild(tr);
    }

    render() {
        return this.div;
    }
}
