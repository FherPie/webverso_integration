from odoo import models
from odoo.exceptions import UserError
import base64


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def webverso_download_pdf(self):
        self.ensure_one()

        report = self.env.ref("sale.action_report_saleorder")

        try:
            pdf, _ = report._render_qweb_pdf(report_ref=report.report_name, res_ids=self.ids)

            return {
                "filename": f"{self.name}.pdf",
                "contentBase64": base64.b64encode(pdf).decode(),
                "mimeType": "application/pdf"
            }

        except Exception as e:
            message = str(e)

            if "Wkhtmltopdf" in message:
                raise UserError(
                    "El servidor Odoo no tiene instalado wkhtmltopdf. No es posible generar PDFs."
                )

            raise UserError(
                f"Error generando el PDF de la cotización SIIII {self.name}: {message}"
            )

    def webverso_portal_link(self):
        self.ensure_one()

        try:
            self._portal_ensure_token()

            relative_url = self.get_portal_url()
            base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")

            if relative_url.startswith("http"):
                portal_url = relative_url
            else:
                portal_url = f"{base_url}{relative_url}"

            return {
                "id": self.id,
                "name": self.name,
                "state": self.state,
                "portalUrl": portal_url
            }

        except Exception as e:
            raise UserError(
                f"Error generando el enlace del portal para {self.name}: {str(e)}"
            )