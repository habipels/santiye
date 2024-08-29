{% if secili_grup.gider_faturasi_gorme_izni %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_gorme_izni" checked class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% else %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_gorme_izni"  class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% endif %}
                                    {% if secili_grup.gider_faturasi_kesme_izni %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_kesme_izni" checked class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% else %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_kesme_izni"  class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% endif %}
                                    {% if secili_grup.gider_faturasi_duzenleme_izni %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_duzenleme_izni" checked class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% else %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_duzenleme_izni"  class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% endif %}
                                    {% if secili_grup.gider_faturasi_silme_izni %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_silme_izni" checked class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% else %}
                                        <td><div class="form-check form-switch"><input name="gider_faturasi_silme_izni"  class="form-check-input toggle-individual" type="checkbox"></div></td>
                                    {% endif %}