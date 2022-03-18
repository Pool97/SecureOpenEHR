//
// Questo file è stato generato dall'architettura JavaTM per XML Binding (JAXB) Reference Implementation, v2.3.0 
// Vedere <a href="https://javaee.github.io/jaxb-v2/">https://javaee.github.io/jaxb-v2/</a> 
// Qualsiasi modifica a questo file andrà persa durante la ricompilazione dello schema di origine. 
// Generato il: 2021.12.31 alle 03:55:01 PM CET 
//


package com.robertopoletti.envprovider;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;
import oasis.names.tc.xacml._3_0.core.schema.wd_17.Attributes;
import org.ow2.authzforce.xmlns.pdp.ext.AbstractAttributeProvider;


/**
 * 
 *                 Test Attribute Provider configuration descriptor. This Provider is used for test purposes only. It can be
 *                 configured to support any attribute but returns always an empty bag as attribute value.
 *             
 * 
 * <p>Classe Java per EnvironmentProviderDescriptor complex type.
 * 
 * <p>Il seguente frammento di schema specifica il contenuto previsto contenuto in questa classe.
 * 
 * <pre>
 * &lt;complexType name="EnvironmentProviderDescriptor"&gt;
 *   &lt;complexContent&gt;
 *     &lt;extension base="{http://authzforce.github.io/xmlns/pdp/ext/3}AbstractAttributeProvider"&gt;
 *       &lt;sequence&gt;
 *         &lt;element ref="{urn:oasis:names:tc:xacml:3.0:core:schema:wd-17}Attributes" maxOccurs="10"/&gt;
 *       &lt;/sequence&gt;
 *     &lt;/extension&gt;
 *   &lt;/complexContent&gt;
 * &lt;/complexType&gt;
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "EnvironmentProviderDescriptor", propOrder = {
    "attributes"
})
public class EnvironmentProviderDescriptor
    extends AbstractAttributeProvider
{

    @XmlElement(name = "Attributes", namespace = "urn:oasis:names:tc:xacml:3.0:core:schema:wd-17", required = true)
    protected List<Attributes> attributes;

    /**
     * Gets the value of the attributes property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the attributes property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getAttributes().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Attributes }
     * 
     * 
     */
    public List<Attributes> getAttributes() {
        if (attributes == null) {
            attributes = new ArrayList<Attributes>();
        }
        return this.attributes;
    }

}
